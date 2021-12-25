from chatbot.db_helper import get_product


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

    def add_product(self, product, quantity) -> None:
        product, _ = get_product(product.id)
        self.items[product.id] = [
            product.name,
            product.description,
            product.get_unit_price(quantity),
            quantity,
        ]

    def get_cart_items(self) -> str:
        return "<br>".join(
            [
                f"{_id}, {self.items[_id][0]}, ${self.items[_id][2]*self.items[_id][3]}, {self.items[_id][3]}"
                for _id in self.items.keys()
            ]
        )
