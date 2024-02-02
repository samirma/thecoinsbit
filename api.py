from coinsbit_api import CoinsBitApi
import json
import coinsbit_api

def print_non_zero_currencies(json_string):
    data = json.loads(json_string)
    result = data.get('result', {})
    
    for currency, details in result.items():
        available = details.get('available', '0')
        
        if available != '0':
            print(f'{currency}: {available}')

api_key = "2ce70369fb64d2dd51107a0769e024aa"
apisecret = "1fcaacdbc7ad7e0e291d6f8900530b2e"


api = CoinsBitApi(api_key, apisecret)


money_balance = api.current_balances("USDT")
#stock_balance = api.current_balances(stock)

stock_balance = ""

print(f"{money_balance}")


api_key = "D8ADDC3A5D843FDBA5265FFE04135E37"
apisecret = "0A2F9292C0321BD767F61445BDE34056"

api = CoinsBitApi(api_key, apisecret)

print("-----------------")

money_balance = api.current_balances("USDT")

print(f"{money_balance}")