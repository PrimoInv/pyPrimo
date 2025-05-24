"""
  Kite account access. All kind of operations via the account:
  - any query on any stock.
"""

from kiteconnect import KiteConnect

class AuthHeader():
    def header_s(self, access):

        global authheader

        authheader = { 
                   'x-device-type' : "WEB",
                   'Authorization' : "Bearer {}".format(access.access_token)
                  }

        return authheader

class TradeRunner(AuthHeader):

    def __init__(self,
                access,
                url = None
                ):

        self.url = url
        self.access_token = access.access_token
        self.app_key = access.app_key
        self.kite = access.kite

        self.kite.set_access_token(self.access_token)


    def instrument_list(self, exchange):

        """Get all stocks under exchange"""
        res = self.kite.instruments(exchange = exchange)
        return res


    def get_stocks_data(self, symbol):

        """Get current price of a stock"""
        # Get quote for the stock
        # Format: EXCHANGE:SYMBOL (e.g., "NSE:RELIANCE")
        quote = self.kite.quote(symbol)

        return quote


def main():
    pass

if __name__ == "__main__":
    # Run the main function
    main()