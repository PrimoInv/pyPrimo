"""
  Find Kite access token.
  - Reads Kite App code from keystrings/1FA.KEY. If found incorrect, ask for manual entry.
  - Save the Access token in keystrings/ACCESS.TOK.
"""

import logging
from _lib.kite.access import Access

# Set up logging
logging.basicConfig(level=logging.INFO)


def access_token():

    try:

        # Initialise Access
        access = Access()

        # Set access token from account url
        access.set_daily_access_token()

    except Exception as e:
        logging.error(f"Kite Access error: {str(e)}")


if __name__ == "__main__":

    # Run the main function
    access_token()