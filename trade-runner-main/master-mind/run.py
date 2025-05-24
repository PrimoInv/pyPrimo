"""
  Run Mastertrust calls.
  - Get Mastertrust App access.
  - Call APIs.
"""

import logging
from _lib.mastertrust.access import Access
from _lib.mastertrust.trade_runner import TradeRunner

URL = 'https://masterswift-beta.mastertrust.co.in'

# Set up logging
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    try:

        # Initialise Access
        access = Access()

        # Initialise trade-runner
        tr = TradeRunner(access, URL)
        access = tr.header_s(access) 

    except Exception as e:
        logging.error(f"TradeRunner Init error: {str(e)}")


    try:

        # fetch stock-price
        instrument_list = tr.instrument_list("NFO")
        with open('output.txt', 'w') as file:
            file.write("Hello/n")
            for key, value in instrument_list.items():
                file.write(f'{key}: {value}\n')

    except Exception as e:
        logging.error(f"Error fetching stock price: {str(e)}")

'''
    try:

        # place order
        order  = tr.place_order(exchange = "NSE",
                                instrument_token = 22,
                                order_side = "BUY",
                                order_type = "LIMIT",
                                product  = "MIS",
                                price =    1000,
                                quantity = 1000,
                                disclosed_quantity = 0,
                                trigger_price = 0,
                                market_protection_percentage = 10,
                                validity ='DAY',
                                user_order_id = 100)

        print(order)

    except Exception as e:
        logging.error(f"Error placing order: {str(e)}")
'''