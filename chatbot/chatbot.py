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
        self.cart = Cart(user.default_shipping_address)

    def set_state_home(self) -> None:
        self.state = HOME
        self.page = 1

    def get_response(self, message) -> str:
        try:
            if message in MAIN_MENU_OPTIONS_LIST:
                option_id = MAIN_MENU_OPTIONS_LIST.index(message.split(" ")[0]) + 1
                return self.get_home_response(option_id)

            if message.strip().isnumeric():
                option = int(message.strip())
                if self.state == HOME:
                    self.set_state_home()
                    return self.get_home_response(option)

                elif self.state == SHOP:
                    return self.get_shop_response(option)

            elif message.startswith("add"):
                if self.state == PRODUCT_DETAILS:
                    quantity = int(message.split(" ")[-1])
                    return self.cart.add_product(self.last_viewed_product, quantity)

            elif message.startswith("remove"):
                if self.state == CART:
                    product_id = int(message.split(" ")[-1])
                    self.cart.remove_product(product_id)
                    return self.get_home_response(4)

            elif message.startswith("update"):
                
                if self.state == CART:
                    message_args = message.split(" ")
                    product_id = int(message_args[1])
                    quantity = int(message_args[2])
                    return self.cart.update_product(
                        product_id, quantity
                    ) + self.get_home_response(4)
                
                elif self.state == SHIPPING_ADDRESS:
                    message_args = message.split(" ")
                    shipping_address = ' '.join(message_args[1:]).strip()
                    self.cart.set_shipping_address(shipping_address)
                    return self.cart.get_shipping_address() 

            # pagination input
            elif message.strip() in ["next", "back"]:
                
                if self.state == SHOP:
                    return self.get_paginated_response(message)
                
                elif self.state == CHECKOUT:
                    # ask for shipping method
                    self.state = SHIPPING_ADDRESS
                    return f"""
                    Your Shipping Address: {self.cart.shiiping_address}<br>
                    Type update new_shipping_address
                    """ + PROCEED
                
                else:
                    pass
            elif message.strip() == "test":
                return self.cart.get_cart_items()
        except:
            pass
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
            self.last_message = self.cart.get_cart_items()
            if self.last_message.strip() == "":
                return NO_MORE_ITEMS
            return self.last_message + REMOVE_FROM_CART + UPDATE_PRODUCT_IN_CART

        elif option == 5:
            # Checkout
            self.state = CHECKOUT
            return self.cart.get_cart_items() + self.cart.get_total_cost() + PROCEED

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