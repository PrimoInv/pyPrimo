"""
  Find access token.
  - Reads App code from keystrings/2FA.KEY. If found incorrect, ask for manual entry.
  - Save the Access token in keystrings/ACCESS.TOK.
"""
import os

cwd = os.chdir("/home/rishi/pyPrimo/trade-runner-main")
import logging
from _lib.mastertrust.access import Access

URL = "https://masterswift-beta.mastertrust.co.in/oauth2/auth?scope=orders%20holdings&state=%7B%22param%22:%22value%22%7D&redirect_uri=https://127.0.0.1&response_type=code&client_id="

# Set up logging
logging.basicConfig(level=logging.INFO)


def access_token():

    try:

        # Initialise Access
        access = Access()

        # Set access token from account url
        access.set_daily_access_token(URL)

    except Exception as e:
        logging.error(f"Mastermind Access error: {str(e)}")


if __name__ == "__main__":

    # Run the main function
    access_token()