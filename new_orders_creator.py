import argparse
from order import *


def calculate_current_spread(highest_bid, lowest_ask):
    spread = lowest_ask - highest_bid
    return spread

def generate_orders(order_type, initial_price, final_price, amount, num_orders):
    price_step = (final_price - initial_price) / (num_orders+1)
    final_list = [Order(order_type, initial_price + (i+1) * price_step, amount) for i in range(num_orders)]
    return final_list

def get_new_orders(bid, ask, spread, base_balance, quote_balance, num_orders, last):
    # Display the current market spread
    current_spread = calculate_current_spread(bid, ask)

    bid_orders = []
    ask_orders = []

    #print(f"Current Market Spread: {current_spread}")
    if (current_spread <= spread):
        print(f"At this point your spread should be less than {current_spread}")
        return bid_orders, ask_orders


    bid_amount_per_order = base_balance / num_orders
    ask_amount_per_order = quote_balance / num_orders

    spread_ref = last * spread

    first_bid_price = last - spread_ref
    first_ask_price = last + spread_ref

    for i in range(num_orders):
        bid_orders.append(Order('bid', first_bid_price - (spread_ref * i), i))
        ask_orders.append(Order('ask', first_ask_price + (spread_ref * i), i))

    # Display the final market spread
    #final_spread = calculate_current_spread(bid_orders[0].price, ask_orders[0].price)

    #print(f"Final Market Spread: {final_spread}")

    return bid_orders, ask_orders

if __name__ == "__main__":
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='Calculate and generate orders based on market data.')
  parser.add_argument('--bid', type=float, help='Current bid price')
  parser.add_argument('--ask', type=float, help='Current ask price')
  parser.add_argument('--last', type=float, help='Last price')
  parser.add_argument('--spread', type=float, help='Desired spread')
  parser.add_argument('--base_balance', type=float, help='Available base currency balance')
  parser.add_argument('--quote_balance', type=float, help='Available quote currency balance')
  parser.add_argument('--num_orders', type=int, help='Number of orders to generate on each side (bid/ask)')

  args = parser.parse_args()

  # Extract arguments and call functions
  bid_orders, ask_orders = get_new_orders(
            bid = args.bid, 
            ask = args.ask, 
            last = args.last,
            spread = args.spread, 
            base_balance = args.base_balance, 
            quote_balance = args.quote_balance,
            num_orders = args.num_orders
            )
  
  print(f"----")
  print(f"Bid Orders:\n", "\n".join(map(str, bid_orders)))
  print(f"bid {args.bid}")
  print(f"Ask Orders:\n", "\n".join(map(str, ask_orders)))
  print(f"ask {args.ask}")



#python3 new_orders_creator.py  --bid  2.12  --ask 2.14	 --last 2.13 --spread 0.005 --base_balance 10 --quote_balance 10 --num_orders 3
