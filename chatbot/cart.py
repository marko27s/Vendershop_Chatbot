from chatbot.db_helper import get_product, get_shipping_method
from constants import *


class Cart:
    """
    For saving items in the cart
    """

    def __init__(self, shiiping_address) -> None:
        self.items = {}
        self.shiiping_address = shiiping_address
        self.shipping_method = None

    def set_shipping_address(self, shiiping_address):
        self.shiiping_address = shiiping_address

    def set_shipping_method(self, shipping_id):
        pass
    
    def get_shipping_address(self):
        return f"""
        Your Shipping Address: {self.shiiping_address}<br>
        Type update new_shipping_address
        """ + PROCEED 

    def remove_product(self, product_id) -> None:
        try:
            del self.items[product_id]
        except:
            pass

    def add_product(self, product, quantity) -> str:
        product, _ = get_product(product.id)
        if product is None:
            return INVALID_PRODUCT_ID

        if product.stock < quantity:
            return STOCK_UNAILABLE

        self.items[product.id] = [
            product.name,
            product.description,
            product.get_unit_price(quantity),
            quantity,
        ]
        return PRODUCT_ADDED_TO_CART

    def update_product(self, product_id, quantity) -> str:
        product, _ = get_product(product_id)
        if product is None:
            return INVALID_PRODUCT_ID

        if product.stock < quantity:
            return STOCK_UNAILABLE

        self.items[product.id] = [
            product.name,
            product.description,
            product.get_unit_price(quantity),
            quantity,
        ]
        return PRODUCT_UPDATED

    def get_cart_items(self) -> str:
        if len(list(self.items.keys())) == 0:
            return ""
        return "-----<br>" + "<br>".join(
            [
                f"{_id}, {self.items[_id][0]}, ${self.items[_id][2]*self.items[_id][3]}, {self.items[_id][3]}"
                for _id in self.items.keys()
            ]
        ) + "<br>-----"

    def get_total_cost(self):
        totals = sum([
            self.items[_id][2]*self.items[_id][3]
            for _id in self.items.keys()
        ])
        return f"""
        <br>
        Total Items Cost: ${totals}
        """

