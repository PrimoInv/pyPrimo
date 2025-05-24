"""
  Access APIs to 
  - access APPs credentials.
  - read login credentials from file.
  - read/write access token from/to file.
"""

from datetime import datetime
import os
import base64
import requests
from _lib.mastertrust.web_interface import fetch_web_access_token
from _common.enc_dec import decrypt

# Daily-generated access-token
ACCESS_TOK_F = '/home/rishi/pyPrimo/trade-runner-main/_keystrings/mastertrust/ACCESS.TOK'
# Kite App API Keys
PRIVATE_KEY_F = '/home/rishi/pyPrimo/trade-runner-main/_keystrings/mastertrust/PRIVATE.KEY'

# Construct the path to the text file in the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

MASTERTRUST_ACCESS_TOKEN_URL = 'https://masterswift-beta.mastertrust.co.in/oauth2/token'
REDIRECT_URI = 'https://127.0.0.1'


class Access():


    def __init__(self):


        self.client_id, self.client_pass, self.totp_key = self.user_credentials()
        print(self.client_id, self.client_pass, self.totp_key)
        self.app_key, self.app_secret = self.app_credentials()


        self.access_token = self.read_access_token()


    def set_daily_access_token(self, _url = None):

        url = _url + self.app_key
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
        if "MUI" in os.environ and "MPW" in os.environ:
            client_id = os.getenv("MUI")
            client_pass = os.getenv("MPW")
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

        return client_id, client_pass, totp_key

        ###if client_pass is not None:
        ###    private_pass = ""
        ###    try:
        ###        private_pass = decrypt(client_pass, pass_key)
        
        ###    except ValueError as e:
        ###        print(f"Error: Invalid hexadecimal string - {e}")

        ###client_pass = private_pass
       
        ###return client_id, client_pass, totp_key
        

    def app_credentials(self):

        # Read API credentials from from file
        with open(PRIVATE_KEY_F, 'r') as file:
            for line in file:
                if '#' not in line and ':' in line:
                    app_credens = line.split(':')
                    return app_credens[4].strip(), app_credens[5].strip()

        return None, None


    def generate_access_token(self):

        # Read app-key from file
        APP_KEY, APP_SECRET = self.app_credentials()

        # generate access-token from request-token and API-secret
        usrPass = f"{APP_KEY}:{APP_SECRET}"
        b64Val = base64.b64encode(usrPass.encode()).decode()

        global headers
        headers = {
                      'Content-Type': 'application/x-www-form-urlencoded',
                      "Authorization": f"Basic {b64Val}",
                    }
        data = {
                'grant_type': 'authorization_code',
                'code': self.request_token,
                'redirect_uri': REDIRECT_URI
                }
        response = requests.post(MASTERTRUST_ACCESS_TOKEN_URL , headers = headers, data = data)
        print(response)
        if 'access_token' in response.json():
            access_token = response.json()['access_token']

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
