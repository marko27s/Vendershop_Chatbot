from vendorshop.product.models import Product

from constants import *


class ChatBot:
    def __init__(self, user) -> None:
        self.user = user
        self.state = HOME
        self.last_message = ""
        self.page = 1

    def get_response(self, message) -> str:

        if message.strip().isnumeric():
            option = int(message.strip())
            if self.state == HOME:
                return self.get_home_response(option)

        # pagination input
        elif message.strip() in ["next", "back"]:
            if self.state == SHOP:
                return self.get_paginated_response(message)

        if message.startswith(HOME.lower()):
            self.state = HOME
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
            products = Product.query.paginate(page=self.page, per_page=3).items
            products_list = [
                f"{p.id} - {p.name} - ${p.min_threshold_amount}" for p in products
            ]
            self.state = SHOP
            self.last_message = "<br>".join(products_list + [SELECT_MESSAGE_BY_ID, PAGINATION])
        else:
            return PARDON

        return self.last_message

    def get_paginated_response(self, option) -> str:
        if self.state == SHOP:
            if option == "next":
                self.page += 1
            else:
                self.page -= 1
            # return products
            products = Product.query.paginate(page=self.page, per_page=3).items
            products_list = [
                f"{p.id} - {p.name} - ${p.min_threshold_amount}" for p in products
            ]
            self.state = SHOP
            self.last_message = "<br>".join(products_list + [SELECT_MESSAGE_BY_ID, PAGINATION])
            return self.last_message
        else:
            return PARDON
