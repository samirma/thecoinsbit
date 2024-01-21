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

bot = CoinsBitApi(api_key, apisecret)

market = "GNC_USDT"

market_result = bot.markets()["result"]

for item in market_result:
    if item['name'] == market:
        print(item)

print(bot.current_balances("USDT")["result"]["USDT"]["available"])
print(bot.current_balances("GNC")["result"]["GNC"]["available"])

ticket = bot.ticker("GNC_USDT")
#print(ticket)
ticket_result = ticket['result']
print(ticket_result)
bid = ticket_result["bid"]
ask = ticket_result["ask"]

#ticket = bot.place_order_buy(currency_pair_code = "GNC_USDT",    amount = "10",  price = "0.5")
#print(ticket)

print(bot.cancel_order(currency_pair_code="GNC_USDT", orderId=24193667596))

