"""
  Trading account access. All kind of operations via the account:
  - any query on any stock.
"""

import requests

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
        self.client_id = access.client_id


    def profile(self):

        url = '{}/api/v1/user/profile?client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def place_order(self,
                   exchange,
                   instrument_token,
                   order_side ,
                   order_type ,
                   product ,
                   price,
                   quantity,
                   disclosed_quantity,
                   trigger_price,
                   market_protection_percentage,
                   validity,
                   user_order_id
                   ):

        params = {
               'exchange'                     : exchange,
               'instrument_token'             : instrument_token,
               'order_side'                   : order_side ,
               'order_type'                   : order_type ,
               'price'                        : price,
               'quantity'                     : quantity,
               'disclosed_quantity'           : disclosed_quantity,
               'product'                      : product ,
               'trigger_price'                : trigger_price,
               'validity'                     : validity,
               'user_order_id'                : user_order_id,
               'client_id'                    : self.client_id,
               'market_protection_percentage' : market_protection_percentage}

        url = '{}/api/v1/orders'.format(self.url)

        res = requests.post(url = url, headers = authheader, data = params)
        res = res.json()
        return res


    def modify_order(self,
                    oms_order_id,
                    instrument_token,
                    exchange,
                    product ,
                    validity,
                    order_type,
                    order_side,
                    price,
                    quantity,
                    disclosed_quantity,
                    client_id
                   ):

        params = {
               'oms_order_id'        : oms_order_id,
               'instrument_token'    : instrument_token,
               'exchange'            : exchange ,
               'product'             : product ,
               'validity'            : validity,
               'order_type'          : order_type,
               'order_side'          : order_side,
               'price'               : price ,
               'quantity'            : quantity,
               'disclosed_quantity'  : disclosed_quantity,
               'client_id'           : client_id
               }

        url = '{}/api/v1/orders'.format(self.url)
        res = requests.put(url = url, headers = authheader, data = params)
        res = res.json()
        return res


    def cancel_normal_order(self, oms_order_id  ):
        url = '{}/api/v1/orders/{}?client_id={} '.format(self.url, oms_order_id, self.client_id)
        res = requests.delete(url = url, headers = authheader)
        res = res.json()
        return res


    def pending_order_book(self):

        url = '{}/api/v1/orders?type=Pending&client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def completed_order_book(self):

        url = '{}/api/v1/orders?type=completed&client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def trading_book(self):

        url = '{}/api/v1/trades?client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def order_history(self,oms_order_id):

        url = '{}/api/v1/order/{}/history?client_id={}'.format(self.url,oms_order_id, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def live_position_book(self):

        url = '{}/api/v1/positions?type=live&client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def all_position_book(self):

        url = '{}/api/v1/positions?type=historical&client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res

    def holdings(self):

        url = '{}/api/v1/holdings?client_id={}'.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res

    def funds(self):

        url = '{}/api/v1/funds/view?client_id={}&type=all '.format(self.url, self.client_id)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def place_bracket_order(self,
                            exchange,
                            instrument_token,
                            market_protection_percentage,
                            order_side ,
                            order_type ,
                            price,
                            square_off_value,
                            stop_loss_value,
                            trailing_stop_loss,
                            quantity,
                            disclosed_quantity,
                            product ,
                            trigger_price,
                            validity,
                            is_trailing,
                            user_order_id,
                            client_id
                            ):

        params = {
                    'exchange'                     : exchange,
                    'instrument_token'             : instrument_token,
                    'order_side'                   : order_side ,
                    'order_type'                   : order_type ,
                    'price'                        : price,
                    'square_off_value'             : square_off_value,
                    'stop_loss_value'              : stop_loss_value,
                    'trailing_stop_loss'           : trailing_stop_loss,
                    'quantity'                     : quantity,
                    'disclosed_quantity'           : disclosed_quantity,
                    'product'                      : product ,
                    'trigger_price'                : trigger_price,
                    'validity'                     : validity,
                    'is_trailing'                  : is_trailing,
                    'user_order_id'                : user_order_id,
                    'client_id'                    : client_id,
                    'market_protection_percentage' : market_protection_percentage}

        url = '{}/api/v1/orders/bracket'.format(self.url)
        res = requests.post(url = url, headers = authheader, data =params)
        res = res.json()
        return res


    def instrument_list(self, exchange):

        """Get all stocks under exchange"""
        url = '{}/api/v2/contracts.json?exchanges={}'.format(self.url,exchange)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


    def script_data(self, token):

        url = '{}/api/v1/marketdata/NSE/Capital?token={}'.format(self.url,token)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res

    def search_script(self, script):

        url = '{}/api/v1/search?key={}'.format(self.url,script)
        res = requests.get(url = url, headers = authheader)
        res = res.json()
        return res


def main():
    pass

if __name__ == "__main__":
    # Run the main function
    main()