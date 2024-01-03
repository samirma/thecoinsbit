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

print(bot.current_balances("USDT"))

print(bot.ticker("GNC_USDT"))