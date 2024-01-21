import argparse
from coinsbit_api import CoinsBitApi
from orders_creator import *

class MarketMakingBot:
    def __init__(self, api, spread, number_of_orders, coin_pair):
        self.api = api
        self.spread = spread
        self.number_of_orders = number_of_orders
        self.coin_pair = coin_pair

    def start(self):
        ticket = self.api.ticker("GNC_USDT")
        ticket_result = ticket['result']
        #print(ticket_result)
        bid = float(ticket_result["bid"])
        ask = float(ticket_result["ask"])

        market_result = self.api.markets()["result"]

        money = ""
        stock = ""

        for item in market_result:
            if item['name'] == self.coin_pair:
                money = item['money']
                stock = item['stock']

        money_balance = float(self.api.current_balances(money)["result"][money]["available"])
        stock_balance = float(self.api.current_balances(stock)["result"][stock]["available"])

        print(f"{money}: {money_balance} {stock} -> {stock_balance}")

        if (money_balance == 0 or stock_balance == 0):
            balance = "Money balance"
            if (stock_balance == 0):
                balance = "Stock balance"

            print(f"{balance} must be higher than 0")
            exit(0)

        bid_orders, ask_orders = get_new_orders(
            bid = bid, 
            ask = ask, 
            spread = self.spread, 
            base_balance = money_balance, 
            quote_balance = stock_balance,
            num_orders = self.number_of_orders
            )
        
        print(f"bid_orders")
        for item in bid_orders:
            print(f"{item}")
        
        print(f"ask_orders")
        for item in ask_orders:
            print(f"{item}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Market Making Bot')
    parser.add_argument('--api_key', required=True, help='API Key')
    parser.add_argument('--api_secret', required=True, help='API Secret')
    parser.add_argument('--spread', type=float, default=0.01, help='Spread')
    parser.add_argument('--number_of_orders', type=int, default=10, help='Number of orders to be placed each side')
    parser.add_argument('--coin_pair', default='USDT_BNB', help='Coin pair to be used')

    args = parser.parse_args()

    #api_key = "2ce70369fb64d2dd51107a0769e024aa"
    #apisecret = "1fcaacdbc7ad7e0e291d6f8900530b2e"

    bot = CoinsBitApi(api_key = args.api_key, api_secret = args.api_secret)

    bot = MarketMakingBot(api=bot, spread=args.spread, number_of_orders=args.number_of_orders, coin_pair=args.coin_pair)
    bot.start()

    #python market_making_bot.py --api_key 2ce70369fb64d2dd51107a0769e024aa --api_secret 1fcaacdbc7ad7e0e291d6f8900530b2e --spread 1 --number_of_orders 3 --coin_pair GNC_USDT
