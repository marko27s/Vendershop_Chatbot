from chatbot.db_helper import get_product
from constants import *


class Cart:
    """
    For saving items in the cart
    """

    def __init__(self) -> None:
        self.items = {}

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
        return "<br>".join(
            [
                f"{_id}, {self.items[_id][0]}, ${self.items[_id][2]*self.items[_id][3]}, {self.items[_id][3]}"
                for _id in self.items.keys()
            ]
        )
