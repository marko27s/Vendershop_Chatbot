import os


MINIMUM_ORDER_VALUE = os.getenv('MINIMUM_ORDER_VALUE', 10)
HOME = "HOME"
SHOP = "SHOP"
PRODUCT_DETAILS = "PRODUCT DETAILS"
ORDERS = "ORDERS"
ORDER_DETAILS = "ORDER_DETAILS"
CART = "CART"
CHECKOUT = "CHECKOUT"
NOTIFICATIONS = "NOTIFICATIONS"
SETTINGS = "SETTINGS"
SHIPPING_ADDRESS = "SHIPPING_ADDRESS"
SHIPPING_METHOD = "SHIPPING_METHOD"
SHIPPING_METHOD_SET = "SHIPPING_METHOD_SET"
PAYMENT_METHOD = "PAYMENT_METHOD"
PAYMENT_METHOD_SET = "PAYMENT_METHOD_SET"
REFUND_ADDRESS = "REFUND_ADDRESS"
REFUND_ADDRESS_SET = "REFUND_ADDRESS_SET"

MAIN_MENU = [
    f"1 {HOME}",
    f"2 {SHOP}",
    f"3 {ORDERS}",
    f"4 {CART}",
    f"5 {CHECKOUT}",
    f"6 {NOTIFICATIONS}",
    f"7 {SETTINGS}",
]
MAIN_MENU_OPTIONS_LIST = [o.lower().split(" ")[1] for o in MAIN_MENU]

PAYMENT_METHODS = {
    1: {"name": "Bitcoin", "value": "btc"},
    2: {"name": "Paypal", "value": "paypal"},
    3: {"name": "Monero", "value": "xmr"},
}

INVALID_PRODUCT_ID = (
    "Invalid Product ID, Please Choose valid Product ID from above list"
)
INVALID_ID = "Invalid ID, Please Choose valid ID from above list"
SELECT_MESSAGE = "Please type any number or the option name from above list"
PAGINATION = "Type next for more or back"
SELECT_MESSAGE_BY_ID = "Please type number from above list to view details"
REQUEST_TO_LOGIN = """
Please specify your username as following
login your_user_name
"""
NO_MORE_ITEMS = "Cart is empty.<br>Type shop for more products."
STOCK_UNAILABLE = (
    "Requested quantity not available, Please choose another quantity.<br><br>"
)
NO_ITEMS_IN_CART = "Cart is empty, Type shop for the products."
ADD_TO_CART = """
<br><br>
To add this product to the cart type following.<br>
add quantity<br>
e.g add 2
"""
REMOVE_FROM_CART = """
<br><br>
Type remove with product ID for removing item from cart.<br>
e.g remove 2
"""
PRODUCT_ADDED_TO_CART = """
Product added to cart.<br><br>
Type shop for more products.
"""
UPDATE_PRODUCT_IN_CART = """
<br><br>
For updating item quantity type following<br>
update product_id new_quantity<br>
e.g update 2 3
"""
PRODUCT_UPDATED = """
<br>
Product updated in cart.<br><br>
"""
PROCEED = """
<br><br>
Type next to proceed.
"""
INPUT_REFUND_ADDRESS = """
Please enter your Refund Address.<br>
"""
REFUND_ADDRESS_SET_AKW = """
Refund Address has been set.
"""
STOCK_NOT_AVAILABLE = """
Stock not available for product {}<br>
Please input another quantity.<br>
"""
MINIMUM_ORDER_VALUE_ERROR = """
<br><br>
Total cost of the items in the cart does not meet the minimum requirements.
Minimum order value is ${}. Please add more items to the cart.<br>
""".format(MINIMUM_ORDER_VALUE)
PARDON = "Pardon, Can you be more specific?"
