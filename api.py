import requests
import time
import base64
import hmac
import hashlib
import json
import apiAccess


# tickers
api_path='/api/v1/account/balance'
request={
    "currency": "USDT",
}
response = apiAccess.authorise(api_path,request)

buy_data= response.text


def print_non_zero_currencies(json_string):
    data = json.loads(json_string)
    result = data.get('result', {})
    
    for currency, details in result.items():
        available = details.get('available', '0')
        
        if available != '0':
            print(f'{currency}: {available}')



print_non_zero_currencies(buy_data)

print(buy_data)
