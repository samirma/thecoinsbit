import requests
import time
import base64
import hmac
import hashlib
import json

import time
import json
import base64

class CoinsBitApi:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://coinsbit.io"
        #Current market endpoints
        self.CURRENT_ORDER_BOOK_ENDPOINT = '/api/v1/public/book'
        self.CURRENT_TICKER_ENDPOINT = '/api/v1/public/ticker'
        
        self.CURRENT_BALANCES_ENDPOINT = "/api/v1/account/balances"
        self.CURRENT_BALANCE_ENDPOINT = "/api/v1/account/balance"
        self.CURRENT_TRANSACTIONS_ENDPOINT = '/api/v1/account/trades'
        self.ORDERS_IN_MARKET_ENDPOINT = '/api/v1/orders'
        self.ORDERS_HISTORY_ENDPOINT = '/api/v1/account/order_history'
        self.TRANSACTIONS_HISTORY_ENDPOINT = '/api/v1/public/history'
        self.PLACE_ORDER_ENDPOINT = '/api/v1/order/new'
        self.CANCEL_ORDER_ENDPOINT = '/api/v1/order/cancel'
        self.CANCEL_PRODUCTS_ENDPOINT = '/api/v1/public/products'

    def authorise(self, api_path, request):
        try:
            complete_url = self.base_url + api_path

            # Add 'request' and 'nonce' to the request dictionary
            request.update({
                'request': api_path,
                'nonce': str(int(time.time()))
            })

            dataJsonStr = json.dumps(request, separators=(',', ':'))
            payload = base64.b64encode(dataJsonStr.encode("ascii"))
            signature = hmac.new(self.api_secret.encode('ascii'), payload, hashlib.sha512).hexdigest()

            # headers for post request
            headers = {"Content-type": "application/json",
                       "X-TXC-APIKEY": self.api_key,
                       "X-TXC-PAYLOAD": payload,
                       "X-TXC-SIGNATURE": signature}
            return requests.post(complete_url, headers=headers, data=dataJsonStr).text

        except Exception as e:
            print('error', e)
            return e
        
    
    def get(self, api_path, params):
        complete_url = self.base_url + api_path
        return requests.get(url = complete_url, params=params).text

    def current_balances(self, currency: str):
        request={
            "currency": currency,
        }
        return self.authorise(api_path = self.CURRENT_BALANCE_ENDPOINT, request = request)
    
    def place_order(self, currency_pair_code: str, side: str = 'sell', amount: str = '0.1', price: str = '0.1'):
        params = {
            "market": currency_pair_code,
            "side": side,
            "amount": amount,
            "price": price
        } 

        return self.authorise(api_path = self.PLACE_ORDER_ENDPOINT, request = params)
    

    def cancel_order(self, currency_pair_code: str, orderId: int):
        params = {
            "market": currency_pair_code,
            "orderId": orderId
        }
        return self.authorise(api_path = self.PLACE_ORDER_ENDPOINT, request = params)
    

    def products(self):
        return self.authorise(api_path = self.CANCEL_PRODUCTS_ENDPOINT, request = {})
    

    def order_book(self, currency_pair_code: str, side: str):
        params = {
            "market": "ETH_BTC",
            "side": "sell"
        }
        return self.get(api_path = self.CURRENT_ORDER_BOOK_ENDPOINT, params = params)
    

    def ticker(self, currency_pair_code: str):
        params = {
            "market": currency_pair_code
        }
        return self.get(api_path = self.CURRENT_TICKER_ENDPOINT, params = params)