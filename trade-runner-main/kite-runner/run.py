"""
  Run Kite calls.
  - Get Kite App access.
  - Call APIs.
"""

import logging
from _lib.kite.access import Access
from _lib.kite.trade_runner import TradeRunner

# Set up logging
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    try:

        # Initialise Access
        access = Access()

        # Initialise trade-runner
        tr = TradeRunner(access)
        access = tr.header_s(access) 

    except Exception as e:
        logging.error(f"TradeRunner Init error: {str(e)}")


    try:

        # fetch stock-price
        instrument_list = tr.instrument_list("NSE")
        print(instrument_list)

    except Exception as e:
        logging.error(f"Error fetching stock price: {str(e)}")
