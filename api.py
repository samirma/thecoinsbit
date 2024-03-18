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

#buy_order = api.place_order_buy(currency_pair_code=pair, amount="0.5", price="0.5")

#print(buy_order)

#print(f"{money_balance}")
#print(api.orders_history())

print(api.order(24193667596))
print(api.order(8946240739))
print(api.order(25602334278))
