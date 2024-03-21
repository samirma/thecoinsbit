import requests
import time
import base64
import hmac
import hashlib
import json

import time
import json
import base64

import logging
import http.client as http_client

# Enable debugging for HTTP connections
if(True):
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

RESULT = "result"
SUCCESS = "success"

class CoinsBitApi:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.coinsbit.io"
        #Current market endpoints
        self.CURRENT_ORDER_BOOK_ENDPOINT = '/api/v1/public/book'
        self.CURRENT_TICKER_ENDPOINT = '/api/v1/public/ticker'

        self.MARKETS_ENDPOINT = '/api/v1/public/markets'
        
        self.CURRENT_BALANCES_ENDPOINT = "/api/v1/account/balances"
        self.CURRENT_BALANCE_ENDPOINT = "/api/v1/account/balance"
        self.CURRENT_TRANSACTIONS_ENDPOINT = '/api/v1/account/trades'
        
        self.ORDERS_HISTORY_ENDPOINT = '/api/v1/account/order_history'
        self.ORDERS_HISTORY_LIST_ENDPOINT = '/api/v1/account/order_history_list'
        self.ORDERS_ORDER_ENDPOINT = '/api/v1/account/order'

        self.TRANSACTIONS_HISTORY_ENDPOINT = '/api/v1/public/history'
        self.PLACE_ORDER_ENDPOINT = '/api/v1/order/new'
        self.CANCEL_ORDER_ENDPOINT = '/api/v1/order/cancel'
        self.CANCEL_PRODUCTS_ENDPOINT = '/api/v1/public/products'

        self.BUY = 'buy'
        self.SELL = 'sell'

    def authorise(self, api_path, params):
        try:
            complete_url = self.base_url + api_path

            # Add 'request' and 'nonce' to the request dictionary
            params.update({
                'request': api_path,
                'nonce': round(time.time() * 1000)
            })

            dataJsonStr = json.dumps(params, separators=(',', ':'))
            payload = base64.b64encode(dataJsonStr.encode("ascii"))
            signature = hmac.new(self.api_secret.encode('ascii'), payload, hashlib.sha512).hexdigest()

            # headers for post request
            headers = {"Content-type": "application/json",
                       "X-TXC-APIKEY": self.api_key,
                       "X-TXC-PAYLOAD": payload,
                       "X-TXC-SIGNATURE": signature}
            return json.loads(requests.post(complete_url, headers=headers, data=dataJsonStr).text)[RESULT]

        except Exception as e:
            print('error', e)
            return e
        
    
    def get(self, api_path, params):
        complete_url = self.base_url + api_path
        return json.loads(requests.get(url = complete_url, params=params).text)[RESULT]

    def current_balances(self, currency: str):
        request={
            "currency": currency,
        }
        return self.authorise(api_path = self.CURRENT_BALANCE_ENDPOINT, params = request)
    
    def place_order(self, currency_pair_code: str, side: str, amount: str, price: str):
        params = {
            "market": currency_pair_code,
            "side": side,
            "amount": amount,
            "price": price
        } 

        return self.authorise(api_path = self.PLACE_ORDER_ENDPOINT, params = params)
    
    def place_order_buy(self, currency_pair_code: str, amount: str, price: str):
        return self.place_order(
                currency_pair_code=currency_pair_code,
                side=self.BUY,
                amount=amount,
                price=price,
            )
    
    def place_order_sell(self, currency_pair_code: str, amount: str, price: str):
        return self.place_order(
                currency_pair_code=currency_pair_code,
                side=self.SELL,
                amount=amount,
                price=price,
            )

    def cancel_order(self, currency_pair_code: str, orderId: int):
        params = {
            "market": currency_pair_code,
            "orderId": orderId
        }
        return self.authorise(api_path = self.CANCEL_ORDER_ENDPOINT, params = params)
    

    def products(self):
        return self.authorise(api_path = self.CANCEL_PRODUCTS_ENDPOINT, params = {})
    

    def order_book(self, currency_pair_code: str, side: str):
        params = {
            "market": currency_pair_code,
            "side": side
        }
        return self.get(api_path = self.CURRENT_ORDER_BOOK_ENDPOINT, params = params)
    

    def ticker(self, currency_pair_code: str):
        params = {
            "market": currency_pair_code
        }
        return self.get(api_path = self.CURRENT_TICKER_ENDPOINT, params = params)
    
    def markets(self):
        return self.get(api_path = self.MARKETS_ENDPOINT, params = {})
    
    
    def orders_history(self):
        params = { }
        return self.authorise(api_path = self.ORDERS_HISTORY_ENDPOINT, params = params)
    
    
    def orders_history_list(self):
        params = { }
        return self.authorise(api_path = self.ORDERS_HISTORY_LIST_ENDPOINT, params = params)
    
    def order(self, order):
        params = {
            "orderId": order
        }
        return self.authorise(api_path = self.ORDERS_ORDER_ENDPOINT, params = params)
    