from vendorshop.product.models import Product

from chatbot.cart import Cart
from chatbot.db_helper import *
from constants import *


class ChatBot:
    def __init__(self, user) -> None:
        self.user = user
        self.state = HOME
        self.last_message = ""
        self.page = 1
        self.last_viewed_product = None
        self.cart = Cart()

    def set_state_home(self) -> None:
        self.state = HOME
        self.page = 1

    def get_response(self, message) -> str:

        if message in MAIN_MENU_OPTIONS_LIST:
            option_id = MAIN_MENU_OPTIONS_LIST.index(message.split(" ")[0]) + 1
            return self.get_home_response(option_id)

        if message.strip().isnumeric():
            option = int(message.strip())
            if self.state == HOME:
                self.set_state_home()
                return self.get_home_response(option)

            if self.state == SHOP:
                return self.get_shop_response(option)

        elif message.startswith("add"):
            if self.state == PRODUCT_DETAILS:
                quantity = int(message.split(" ")[-1])
                self.cart.add_product(self.last_viewed_product, quantity)
                return PRODUCT_ADDED_TO_CART
        
        elif message.startswith("remove"):
            if self.state == CART:
                product_id = int(message.split(" ")[-1])
                self.cart.remove_product(product_id)
                return self.cart.get_cart_items()

        # pagination input
        elif message.strip() in ["next", "back"]:
            if self.state == SHOP:
                return self.get_paginated_response(message)

        elif message.strip() == "test":
            return self.cart.get_cart_items()

        return PARDON

    def get_home_response(self, option) -> str:
        if option == 1:
            self.state = HOME
            self.last_message = "<br>".join(MAIN_MENU + [SELECT_MESSAGE])

        elif option == 2:
            # return products
            self.page = 1
            self.page, self.last_message = get_products(self.page, "")
            self.state = SHOP

        elif option == 4:
            # return cart items
            self.state = CART
            return self.cart.get_cart_items()
       
        else:
            return PARDON

        return self.last_message

    def get_shop_response(self, option) -> str:
        self.state = PRODUCT_DETAILS
        self.last_viewed_id = int(option)
        self.last_viewed_product, self.last_message = get_product(option)
        return self.last_message

    def get_paginated_response(self, option) -> str:
        if self.state == SHOP:
            # return products
            self.page, self.last_message = get_products(self.page, option)
            self.state = SHOP
            return self.last_message
        else:
            return PARDON
