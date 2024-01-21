import argparse
from CoinsBitApi import CoinsBitApi

class MarketMakingBot:
    def __init__(self, api_key, api_secret, spread, number_of_orders, coin_pair):
        self.api = CoinsBitApi(api_key, api_secret)
        self.spread = spread
        self.number_of_orders = number_of_orders
        self.coin_pair = coin_pair

    def start(self):
        # Cancel all existing orders
        existing_orders = self.api.get_all_orders(self.coin_pair)
        for order in existing_orders:
            self.api.cancel_order(self.coin_pair, order['id'])

        # Get the current market price
        ticker = self.api.ticker(self.coin_pair)
        mid_price = (ticker['bid'] + ticker['ask']) / 2

        # Get the available balance for each coin
        base_coin, quote_coin = self.coin_pair.split('_')
        base_balance = self.api.current_balances(base_coin)
        quote_balance = self.api.current_balances(quote_coin)

        # Calculate the amount for each order
        base_amount = base_balance / self.number_of_orders
        quote_amount = quote_balance / (self.number_of_orders * mid_price)

        # Calculate the price for each order and place the orders
        for i in range(self.number_of_orders):
            buy_price = mid_price * (1 - self.spread * (i + 1))
            sell_price = mid_price * (1 + self.spread * (i + 1))
            self.api.place_order(self.coin_pair, 'buy', quote_amount, buy_price)
            self.api.place_order(self.coin_pair, 'sell', base_amount, sell_price)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Market Making Bot')
    parser.add_argument('--api_key', required=True, help='API Key')
    parser.add_argument('--api_secret', required=True, help='API Secret')
    parser.add_argument('--spread', type=float, default=0.01, help='Spread')
    parser.add_argument('--number_of_orders', type=int, default=10, help='Number of orders to be placed each side')
    parser.add_argument('--coin_pair', default='USDT_BNB', help='Coin pair to be used')

    args = parser.parse_args()

    bot = MarketMakingBot(args.api_key, args.api_secret, args.spread, args.number_of_orders, args.coin_pair)
    bot.start()
