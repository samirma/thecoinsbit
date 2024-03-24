class Order:
    def __init__(self, order_type, price, amount, id=-1):
        self.order_type = order_type
        self.price = price
        self.amount = amount
        self.id = id

    def __repr__(self):
        return f"Order(id={self.id}, order_type='{self.order_type}', price={self.price}, amount={self.amount})"


def get_order(json_data):
    """
    Maps JSON data representing an order to an Order object.

    Args:
        json_data (dict): JSON data containing order information.

    Returns:
        Order: An Order object populated with the data from the JSON.
    """

    order_type = json_data.get("side", None)  # Handle potential missing key
    price = float(json_data.get("price", 0.0))  # Convert price to float and set default
    amount = float(json_data.get("amount", 0.0))  # Convert amount to float and set default
    order_id = json_data.get("orderId", -1)  # Get id or use default
    order = Order(order_type, price, amount, order_id)
    print(f"Order {json_data['amount']} {json_data['dealMoney']} {json_data['dealStock']} ")
    return order
