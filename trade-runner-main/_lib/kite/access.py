"""
  Access APIs to 
  - access APPs credentials.
  - read login credentials from file.
  - read/write access token from/to file.
"""

from kiteconnect import KiteConnect
from datetime import datetime
import os
from _lib.kite.web_interface import fetch_web_access_token
from _common.enc_dec import decrypt

# Daily-generated access-token
ACCESS_TOK_F = '../_keystrings/kite/ACCESS.TOK'
# Kite App API Keys
PRIVATE_KEY_F = '../_keystrings/kite/PRIVATE.KEY'

# Construct the path to the text file in the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)


class Access():


    def __init__(self):

        self.client_id, self.client_pass, self.totp_key = self.user_credentials()

        self.app_key, self.app_secret = self.app_credentials()

        self.access_token = self.read_access_token()

        self.kite = self.kite_access()


    def set_daily_access_token(self, _url = None):

        url = self.account_url() ## Fetch account url
        print(f"url: {url}")

        self.request_token = fetch_web_access_token(url, self.client_id, self.client_pass, self.totp_key)

        self.access_token = self.generate_access_token()
            
        self.save_access_token()


    def user_credentials(self):

        client_id = None
        client_pass = None
        totp_key = None
        pass_key = None

        """Read login credens from environment"""
        if "ZZUI" in os.environ and "ZPW" in os.environ:
            client_id = os.getenv("ZUI")
            client_pass = os.getenv("ZPW")
        else:
            # Read User credentials from from file
            with open(PRIVATE_KEY_F, 'r') as file:
                for line in file:
                    if line.strip().startswith("#"):
                        continue
                    app_credens = line.split(':')
                    client_id = app_credens[0].strip()
                    client_pass = app_credens[1].strip()

        # Read TOTP Key from from file
        with open(PRIVATE_KEY_F, 'r') as file:
            for line in file:
                if line.strip().startswith("#"):
                    continue
                app_credens = line.split(':')
                totp_key = app_credens[2].strip()
                pass_key = app_credens[6].strip() if len(app_credens) > 6 and app_credens[6].strip() != '' else None

        if client_pass is not None:
            private_pass = ""
            try:
                private_pass = decrypt(client_pass, pass_key)
        
            except ValueError as e:
                print(f"Error: Invalid hexadecimal string - {e}")

        client_pass = private_pass

        return client_id, client_pass, totp_key

    
    def app_credentials(self):

        # Read API credentials from from file
        with open(PRIVATE_KEY_F, 'r') as file:
            for line in file:
                if '#' not in line and ':' in line:
                    app_credens = line.split(':')
                    return app_credens[4].strip(), app_credens[5].strip()

        return None, None


    def generate_access_token(self):

        # generate access-token from request-toek and API-secret
        data = self.kite.generate_session(self.request_token, api_secret=self.app_secret)
        access_token = data["access_token"]

        return access_token


    def save_access_token(self):

        # Get current timestamp as a datetime object
        current_time = datetime.now()
        # Format as string (e.g., DDMMYYYYHHMMSS)
        formatted_ts = current_time.strftime("%d%m%Y%H%M%S")

        # Save access token to file
        with open(ACCESS_TOK_F, "w") as f:
            f.write(f"{formatted_ts}:{self.access_token}")
            f.close()
        
        return self.access_token


    def read_access_token(self):

        # Read access token from file
        with open(ACCESS_TOK_F, "r") as f:
            ts_access_token = f.read()
            parts = ts_access_token.split(':')
            access_token = parts[1] if len(parts) > 1 else None
            f.close()
        
        return access_token


    def kite_access(self):

        # Get Kite account url from App API Key
        kite = KiteConnect(api_key = self.app_key)

        return kite


    def account_url(self):

        # Get Kite account url from App API Key
        url = self.kite.login_url()

        return url

