from vendorshop.product.models import Product

from chatbot.db_helper import *
from constants import *


class ChatBot:
    def __init__(self, user) -> None:
        self.user = user
        self.state = HOME
        self.last_message = ""
        self.page = 1

    def set_state_home(self) -> None:
        self.state = HOME
        self.page = 1

    def get_response(self, message) -> str:

        if message.strip().isnumeric():
            option = int(message.strip())
            if self.state == HOME:
                self.set_state_home()
                return self.get_home_response(option)

            if self.state == SHOP:
                return self.get_shop_response(option)

        # pagination input
        elif message.strip() in ["next", "back"]:
            if self.state == SHOP:
                return self.get_paginated_response(message)

        if message.startswith(HOME.lower()):
            self.set_state_home()
            self.last_message = "<br>".join(MAIN_MENU + [SELECT_MESSAGE])
            return self.last_message
        elif message.startswith(SHOP.lower()):
            self.state = SHOP
            return self.get_home_response(2)

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
        else:
            return PARDON

        return self.last_message

    def get_shop_response(self, option) -> str:
        self.state = PRODUCT_DETAILS
        self.last_message = get_product(option)
        return self.last_message

    def get_paginated_response(self, option) -> str:
        if self.state == SHOP:
            # return products
            self.page, self.last_message = get_products(self.page, option)
            self.state = SHOP
            return self.last_message
        else:
            return PARDON
