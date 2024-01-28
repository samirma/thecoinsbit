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

coin_pair = "GNC_USDT"

market_result = api.markets()["result"]

#print(market_result)

money = ""
stock = ""

for item in market_result:
    if item['name'] == coin_pair:
        money = item['money']
        stock = item['stock']
        print(item)

#money_balance = float(api.current_balances(money)["result"][money]["available"])
#stock_balance = float(api.current_balances(stock)["result"][stock]["available"])

money_balance = api.current_balances(money)
#stock_balance = api.current_balances(stock)

stock_balance = ""

print(f"{money}: {money_balance} {stock} -> {stock_balance}")