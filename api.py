from coinsbit_api import CoinsBitApi
import json
import env 

def print_non_zero_currencies(json_string):
    data = json.loads(json_string)
    result = data.get('result', {})

    for currency, details in result.items():
        available = details.get('available', '0')

        if available != '0':
            print(f'{currency}: {available}')

# Load keys from a separate configuration file
api_key = env.api_key
apisecret = env.apisecret

pair = "GNC_USDT"

api = CoinsBitApi(api_key, apisecret)

money_balance = api.current_balances("USDT")
stock_balance = ""

buy_order = api.place_order_buy(currency_pair_code=pair, amount="0.5", price="0.5")

orderId = buy_order["orderId"]
print(api.order(orderId))


print("canceled")
print("canceled")
print("canceled")
print("canceled")
print("canceled")
print("canceled")
canceled = api.cancel_order(pair, orderId)
print("canceled")
print("canceled")
print("canceled")
print("canceled")
print("canceled")
print("canceled")


print(canceled)

print(api.order(orderId))