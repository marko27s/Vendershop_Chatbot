from vendorshop.admin.models import Notification
from vendorshop.product.models import Product

from chatbot.cart import Cart
from chatbot.db_helper import *
from constants import *


class ChatBot:
    def __init__(self, user) -> None:
        self.user = user
        self.state = HOME
        self.last_message = ""
        self.last_id = None
        self.page = 1
        self.last_viewed_product = None
        self.ticket_sub = ""
        self.ticket_msg = ""
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

                elif self.state == SHIPPING_METHOD:
                    self.last_message = self.cart.set_shipping_method(option)
                    if self.last_message == INVALID_ID:
                        return INVALID_ID
                    self.state = SHIPPING_METHOD_SET
                    return self.last_message

                elif self.state == PAYMENT_METHOD:
                    self.last_message = self.cart.set_payment_method(option)
                    if self.last_message == INVALID_ID:
                        return INVALID_ID
                    self.state = PAYMENT_METHOD_SET
                    return self.last_message

                elif self.state == ORDERS:
                    self.state = ORDER_DETAILS
                    self.last_id = option
                    return get_order_by_id(option, self.user.id)

                elif self.state == ORDER_DETAILS:
                    # 1 - start ticket flow
                    if option == 1:
                        self.state = CREATE_TICKET
                        return CREATE_TICKET_CONFIRM.format(self.last_id)

                elif self.state == CREATE_TICKET_CONFIRM:
                    self.state = SELECT_ITEM_ID
                    self.last_id = option
                    return CREATE_TICKET_SUBKECT

                elif self.state == TICKETS:
                    self.state = TICKET_DETAILS
                    self.last_id = option
                    return get_ticket_from_id(self.user.id, option)
                else:
                    pass

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
                    shipping_address = " ".join(message_args[1:]).strip()
                    self.cart.set_shipping_address(shipping_address)
                    return self.cart.get_shipping_address()

            # pagination input
            elif message.strip() in ["next", "back"]:

                if self.state == SHOP:
                    return self.get_paginated_response(message)

                elif self.state == ORDERS:
                    self.page, self.last_message = get_order_by_user(
                        self.user.id, self.page, message
                    )
                    return self.last_message

                elif self.state == TICKETS:
                    self.page, self.last_message = get_all_tickets_for_the_user(
                        self.user.id, self.page, message
                    )
                    return self.last_message

                elif self.state == CHECKOUT:
                    # ask for shipping method
                    self.state = SHIPPING_ADDRESS
                    return (
                        f"""
                    Your Shipping Address: {self.cart.shiiping_address}<br>
                    Type update new_shipping_address
                    """
                        + PROCEED
                    )

                elif self.state == SHIPPING_ADDRESS:
                    self.state = SHIPPING_METHOD
                    return get_shipping_methods()

                elif self.state == SHIPPING_METHOD_SET:
                    self.state = PAYMENT_METHOD
                    return get_payment_methods()

                elif self.state == PAYMENT_METHOD_SET:
                    self.state = REFUND_ADDRESS
                    return INPUT_REFUND_ADDRESS

                elif self.state == REFUND_ADDRESS_SET:
                    # Create order here
                    self.state = ORDER_CREATED
                    return self.cart.create_order(self.user)

                elif self.state == NOTIFICATIONS:
                    # return paginated notifications
                    (
                        self.page,
                        self.last_message,
                    ) = get_latest_notifications_for_the_user(
                        self.user, self.page, message
                    )
                    return self.last_message

                elif self.state == PRODUCT_DETAILS:
                    if message == "next":
                        return PARDON
                    else:
                        return self.get_home_response(2)

                elif self.state == ORDER_DETAILS:
                    if message == "next":
                        return PARDON
                    else:
                        return self.get_home_response(3)
                else:
                    pass

            elif message in ["yes"]:

                if self.state == CREATE_TICKET:
                    self.state = CREATE_TICKET_CONFIRM
                    return get_items_by_order_id(self.last_id, self.user.id)

            elif len(message) > 5:
                if self.state == REFUND_ADDRESS:
                    self.state = REFUND_ADDRESS_SET
                    return self.cart.set_refund_address(message.strip())

                elif self.state == SELECT_ITEM_ID:
                    self.state = CREATE_TICKET_SUBKECT
                    self.ticket_sub = message
                    return CREATE_TICKET_MESSAGE

                elif self.state == CREATE_TICKET_SUBKECT:
                    self.state == CREATE_TICKET_CONFIRM
                    self.ticket_msg = message

                    return create_ticket_for_the_order(
                        self.user.id, self.last_id, self.ticket_sub, self.ticket_msg
                    )

                elif self.state == TICKET_DETAILS:
                    # reply to ticket
                    return send_message_for_ticket(self.last_id, message)

            elif message.strip() == "test":
                return self.cart.get_cart_items()
        except Exception as e:
            print(e)
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

        elif option == 3:
            self.page = 1
            self.state = ORDERS
            self.page, self.last_message = get_order_by_user(
                self.user.id, self.page, option
            )
            return self.last_message

        elif option == 4:
            # return cart items
            self.state = CART
            self.last_message = self.cart.get_cart_items()
            if self.last_message.strip() == "":
                return NO_MORE_ITEMS
            return self.last_message + REMOVE_FROM_CART + UPDATE_PRODUCT_IN_CART

        elif option == 5:
            # Checkout
            if self.cart.total_cost() < MINIMUM_ORDER_VALUE:
                return self.cart.get_cart_items() + MINIMUM_ORDER_VALUE_ERROR
            self.state = CHECKOUT
            return self.cart.get_cart_items() + self.cart.get_total_cost() + PROCEED

        elif option == 6:
            # Notifications
            self.state = NOTIFICATIONS
            self.page = 1
            self.page, self.last_message = get_latest_notifications_for_the_user(
                self.user, self.page, option
            )
            return self.last_message

        elif option == 7:
            # Tickets
            self.state = TICKETS
            self.page = 1
            _, self.last_message = get_all_tickets_for_the_user(
                self.user.id, self.page, ""
            )
            return self.last_message
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
