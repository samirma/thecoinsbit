import argparse

class Order:
    def __init__(self, order_type, price, amount):
        self.order_type = order_type
        self.price = price
        self.amount = amount

    def __repr__(self):
        return f"Price = {self.price}, amount = {self.amount}"

def calculate_current_spread(highest_bid, lowest_ask):
    spread = lowest_ask - highest_bid
    return spread

def generate_orders(order_type, initial_price, final_price, amount, num_orders):
    price_step = (final_price - initial_price) / (num_orders+1)
    final_list = [Order(order_type, initial_price + (i+1) * price_step, amount) for i in range(num_orders)]
    return final_list

def get_new_orders(bid, ask, spread, base_balance, quote_balance, num_orders):
    # Display the current market spread
    current_spread = calculate_current_spread(bid, ask)
    print(f"Current Market Spread: {current_spread}")
    if (current_spread <= spread):
        print(f"At this point your spread should be less than {current_spread}")
        exit(0)

    bid_orders = []
    ask_orders = []
    bid_amount_per_order = base_balance / num_orders
    ask_amount_per_order = quote_balance / num_orders

    # Calculate the first order price
    mid_price = (bid + ask) / 2
    first_bid_price = mid_price - (spread / 2)
    first_ask_price = mid_price + (spread / 2)

    bid_orders.append(Order('bid', first_bid_price, bid_amount_per_order))
    ask_orders.append(Order('ask', first_ask_price, ask_amount_per_order))
    if (num_orders > 1):
        bid_orders = bid_orders + (generate_orders('bid', first_bid_price, bid, bid_amount_per_order, (num_orders-1)))
        ask_orders = ask_orders + (generate_orders('ask', first_ask_price, ask, ask_amount_per_order, (num_orders-1)))

    # Display the final market spread
    final_spread = calculate_current_spread(bid_orders[0].price, ask_orders[0].price)

    print(f"Final Market Spread: {final_spread}")

    return bid_orders, ask_orders

if __name__ == "__main__":
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='Calculate and generate orders based on market data.')
  parser.add_argument('--bid', type=float, help='Current bid price')
  parser.add_argument('--ask', type=float, help='Current ask price')
  parser.add_argument('--spread', type=float, help='Desired spread')
  parser.add_argument('--base_balance', type=float, help='Available base currency balance')
  parser.add_argument('--quote_balance', type=float, help='Available quote currency balance')
  parser.add_argument('--num_orders', type=int, help='Number of orders to generate on each side (bid/ask)')

  args = parser.parse_args()

  # Extract arguments and call functions
  bid_orders, ask_orders = get_new_orders(args.bid, args.ask, args.spread, args.base_balance, args.quote_balance, args.num_orders)
  print(f"----")
  print(f"Bid Orders:\n", "\n".join(map(str, bid_orders)))
  print(f"bid {args.bid}")
  print(f"Ask Orders:\n", "\n".join(map(str, ask_orders)))
  print(f"ask {args.ask}")
