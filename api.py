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

buy_order = api.place_order_sell(currency_pair_code=pair, amount="0.5", price="10.5")
orderId = buy_order["orderId"]
print(f'###### place_order_buy {orderId}')

def show_history():
    #print("###### orders_history")
    #print(api.orders_history(offset=0, limit=1000))
    #print("###### orders_history_list")
    #print(api.orders_history_list(offset=0, limit=1000))
    print("###### orders")
    print(api.orders(pair))

all_orders = []
def continue_paging(orders, limit_result, offset_result, total_result):
    print(f'###### continue_paging {len(orders)} {limit_result}, {offset_result}, {total_result}')
    all_orders.extend(orders)
    return True

api.paginate_orders(pair_code=pair, continue_paging_lambda=continue_paging)

for ord in all_orders:
    ordId = ord["id"]
    print(f'ord {ord["id"]}')  
    api.cancel_order(pair, ordId)