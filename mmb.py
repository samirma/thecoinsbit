import argparse
import time
import math
from typing import Tuple

import requests

from coinsbit_api import CoinsBitApi  # Import the CoinsBit API client

# Function to calculate order prices based on mid-price and spread
def calculate_order_prices(mid_price: float, spread: float, base_amount: float) -> Tuple[float, float]:
    half_spread = spread / 2
    bid_price = mid_price - half_spread
    ask_price = mid_price + half_spread

    # Adjust prices to ensure a minimum profit for each trade
    bid_price = max(bid_price, ask_price - base_amount * spread)
    ask_price = min(ask_price, bid_price + base_amount * spread)

    return bid_price, ask_price

# Function to manage orders and positions
def manage_orders(api: CoinsBitApi, pair: str, spread: float, base_balance: float, quote_balance: float, num_orders: int) -> None:
    mid_price = api.ticker(pair)["last"]
    bid_price, ask_price = calculate_order_prices(mid_price, spread, base_balance / num_orders)

    # Get existing orders and balances
    existing_orders = api.orders_history_list()
    base_balance = api.current_balances(pair.split("_")[1])["balance"]
    quote_balance = api.current_balances(pair.split("_")[0])["balance"]

    # Cancel existing orders if necessary
    for order in existing_orders:
        if order["market"] == pair:
            api.cancel_order(pair, order["id"])

    # Place new orders
    for i in range(num_orders):
        api.place_order_buy(pair, base_balance / num_orders, str(bid_price))
        api.place_order_sell(pair, quote_balance / num_orders, str(ask_price))

# Main function
def main():
    parser = argparse.ArgumentParser(description="CoinsBit Market Maker Bot")
    parser.add_argument("--pair", type=str, required=True, help="The currency pair to trade")
    parser.add_argument("--spread", type=float, required=True, help="The spread between buy and sell orders")
    parser.add_argument("--base_balance", type=float, required=True, help="The initial balance of the base currency")
    parser.add_argument("--quote_balance", type=float, required=True, help="The initial balance of the quote currency")
    parser.add_argument("--num_orders", type=int, default=3, help="The number of orders to place on each side")
    parser.add_argument("--delay", type=int, default=500, help="The delay between order placement in milliseconds")
    args = parser.parse_args()

    api_key = input("Enter your CoinsBit API key: ")
    api_secret = input("Enter your CoinsBit API secret: ")

    api = CoinsBitApi(api_key, api_secret)

    while True:
        try:
            manage_orders(api, args.pair, args.spread, args.base_balance, args.quote_balance, args.num_orders)
            time.sleep(args.delay / 1000)  # Delay in seconds
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Retry after a brief delay

if __name__ == "__main__":
    main()
