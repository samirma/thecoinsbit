import argparse
from coinsbit_api import CoinsBitApi
from orders_creator import *
import env 
import time

class MarketMakingBot:
    def __init__(self, api, spread, number_of_orders, coin_pair, delay):
        self.api = api
        self.spread = spread
        self.number_of_orders = number_of_orders
        self.coin_pair = coin_pair
        self.delay = delay
    
    def cancel_orders(self):
        existing_orders = self.api.orders_history_list()

        # Cancel existing orders if necessary
        for order in existing_orders:
            if order["market"] == self.coin_pair:
                print(order)
                #self.api.cancel_order(self.coin_pair, order["id"])

    def manage_orders(self):
        ticket = self.api.ticker(self.coin_pair)
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

        self.cancel_orders()

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

    
    def start(self):
        while True:
            try:
                self.manage_orders()
                time.sleep(self.delay / 1000)  # Delay in seconds
            except Exception as e:
                print(f"An error occurred: {e}")
                exit(0)


if __name__ == "__main__":

    api_key = env.api_key
    api_secret = env.apisecret

    parser = argparse.ArgumentParser(description='Market Making Bot')
    parser.add_argument('--spread', type=float, default=0.01, help='Spread')
    parser.add_argument('--orders', type=int, default=10, help='Number of orders to be placed each side')
    parser.add_argument('--pair', default='USDT_BNB', help='Coin pair to be used')
    parser.add_argument('--delay', type=int, default=1, help='Delay in seconds')

    args = parser.parse_args()

    #api_key = "2ce70369fb64d2dd51107a0769e024aa"
    #apisecret = "1fcaacdbc7ad7e0e291d6f8900530b2e"

    bot = CoinsBitApi(api_key = api_key, api_secret = api_secret)

    bot = MarketMakingBot(api=bot, spread=args.spread, number_of_orders=args.orders, coin_pair=args.pair, delay=args.delay)
    bot.start()

    #python market_making_bot.py --api_key 2ce70369fb64d2dd51107a0769e024aa --api_secret 1fcaacdbc7ad7e0e291d6f8900530b2e --spread 1 --number_of_orders 3 --coin_pair GNC_USDT
