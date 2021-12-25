HOME = "HOME"
SHOP = "SHOP"
PRODUCT_DETAILS = "PRODUCT DETAILS"
ORDERS = "ORDERS"
CART = "CART"
CHECKOUT = "CHECKOUT"
NOTIFICATIONS = "NOTIFICATIONS"
SETTINGS = "SETTINGS"

MAIN_MENU = [
    f"1 {HOME}",
    f"2 {SHOP}",
    f"3 {ORDERS}",
    f"4 {CART}",
    f"5 {CHECKOUT}",
    f"6 {NOTIFICATIONS}",
    f"7 {SETTINGS}",
]
MAIN_MENU_OPTIONS_LIST = [o.lower().split(' ')[1] for o in MAIN_MENU]
INVALID_PRODUCT_ID = (
    "Invalid Product ID, Please Choose valid Product ID from above list"
)
SELECT_MESSAGE = "Please type any number or the option name from above list"
PAGINATION = "Type next for more or back"
SELECT_MESSAGE_BY_ID = "Please type number from above list to view details"
REQUEST_TO_LOGIN = """
Please specify your username as following
login your_user_name
"""
NO_MORE_ITEMS = 'No more items.'
PRODUCT_ADDED_TO_CART = """
Product added to cart.<br><br>
Type shop for more products.
"""
PARDON = "Pardon, Can you be more specific?"
