import argparse
from coinsbit_api import CoinsBitApi
from orders_creator import *
import env 
import time
from order import *
from datetime import datetime

class MarketMakingBot:
    def __init__(self, api, spread, number_of_orders, coin_pair, delay, money_limit, stock_limit):
        self.api: CoinsBitApi = api
        self.spread = spread
        self.number_of_orders = number_of_orders
        self.coin_pair = coin_pair
        self.delay = delay
        self.money_limit = money_limit
        self.stock_limit = stock_limit
    
    def cancel_orders(self):
        all_orders = []
        def continue_paging(orders, limit_result, offset_result, total_result):
            #print(f'###### continue_paging {len(orders)} {limit_result}, {offset_result}, {total_result}')
            all_orders.extend(orders)
            return True

        self.api.paginate_orders(pair_code=self.coin_pair, continue_paging_lambda=continue_paging)

        for ord in all_orders:
            ordId = ord["id"]
            #print(f'Cancelling {ord["id"]}')  
            self.api.cancel_order(self.coin_pair, ordId)

        return len(all_orders)


    def check_balances(self, money_balance, stock_balance):
        if (money_balance == 0 or stock_balance == 0):
            balance = "Money balance"
            if (stock_balance == 0):
                balance = "Stock balance"

            print(f"{balance} must be higher than 0")
            exit(0)


        if (self.money_limit > 0 and money_balance < self.money_limit):
            balance = "Money balance"
            print(f"{balance} must be higher than {self.money_limit}")
            exit(0)

        if (self.stock_limit > 0 and stock_balance < self.stock_limit):
            balance = "Stock balance"
            print(f"{balance} must be higher than {self.stock_limit}")
            exit(0)

    def manage_orders(self):
        canceled_count = self.cancel_orders()

        if (canceled_count > 0):
            print(f"sleep after canceled {canceled_count} orders")
            time.sleep(1)

        ticket_result = self.api.ticker(self.coin_pair)
        
        #print(ticket_result)
        bid = float(ticket_result["bid"])
        ask = float(ticket_result["ask"])

        self.check_spread()

        market_result = self.api.markets()

        money = ""
        stock = ""

        for item in market_result:
            if item['name'] == self.coin_pair:
                money = item['money']
                stock = item['stock']

        money_balance = float(self.api.current_balances(money)["available"])
        stock_balance = float(self.api.current_balances(stock)["available"])

        #print(f"{money}: {money_balance} {stock} -> {stock_balance}")

        self.check_balances(money_balance, stock_balance)

        if (self.money_limit > 0):
            money_balance = self.money_limit 

        if (self.stock_limit > 0):
            stock_balance = self.stock_limit

        bid_orders, ask_orders = get_new_orders(
            bid = bid, 
            ask = ask, 
            spread = self.spread, 
            base_balance = money_balance, 
            quote_balance = stock_balance,
            num_orders = self.number_of_orders
            )
        
        #print(f"bid_orders")
        for item in bid_orders:
            #print(f"{item}")
            self.api.place_order_buy(currency_pair_code=self.coin_pair, amount=item.amount, price=item.price)
        
        #print(f"ask_orders")
        for item in ask_orders:
            #print(f"{item}")
            self.api.place_order_sell(currency_pair_code=self.coin_pair, amount=item.amount, price=item.price)
        
    
    def start(self):
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Loop started at {current_time}")
            self.manage_orders()
            time.sleep(self.delay)  # Delay in seconds
            #return

    def check_spread(self):
        ticket_result = self.api.ticker(self.coin_pair)
        bid = float(ticket_result["bid"])
        ask = float(ticket_result["ask"])
        current_spread = calculate_current_spread(bid, ask)
        print(f'current_spread {current_spread} bid: {bid} ask: {ask}')  


if __name__ == "__main__":

    api_key = env.api_key
    api_secret = env.apisecret

    parser = argparse.ArgumentParser(description='Market Making Bot')
    parser.add_argument('--spread', type=float, default=0.01, help='Spread')
    parser.add_argument('--orders', type=int, default=10, help='Number of orders to be placed each side')
    parser.add_argument('--pair', default='USDT_BNB', help='Coin pair to be used')

    parser.add_argument('--money_limit', type=float, default=1, help='Money limit to be used')
    parser.add_argument('--stock_limit', type=float, default=1, help='Stock limit to be used')

    parser.add_argument('--delay', type=int, default=1, help='Delay in seconds')

    args = parser.parse_args()

    #api_key = "2ce70369fb64d2dd51107a0769e024aa"
    #apisecret = "1fcaacdbc7ad7e0e291d6f8900530b2e"

    bot = CoinsBitApi(api_key = api_key, api_secret = api_secret)

    bot = MarketMakingBot(api=bot, spread=args.spread, number_of_orders=args.orders, coin_pair=args.pair, delay=args.delay, money_limit=args.money_limit, stock_limit=args.stock_limit)


    bot.start()

    bot.check_spread()

    #python market_making_bot.py --spread 1 --number_of_orders 3 --coin_pair GNC_USDT --money_limit 10  --stock_limit 10
