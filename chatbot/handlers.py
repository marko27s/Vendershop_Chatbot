from chatbot.db_helper import *
from constants import *


def get_home_response(message, user_state):

    # set page to 1
    user_state["page"] = 1

    # if numeric then its already main menu option id
    # else convert message into main menu option id
    if str(message).isnumeric():
        message = int(message)
    else:
        message = MAIN_MENU_OPTIONS_LIST.index(str(message).split(" ")[0]) + 1

    if message == 1:
        # return main menu
        state = HOME
        response = "<br>".join(MAIN_MENU + [SELECT_MESSAGE])

    elif message == 2:
        # return products
        state = SHOP
        user_state["page"], response = get_products(user_state["page"], "")

    elif message == 3:
        state = ORDERS
        _, response = get_order_list(message, user_state)

    elif message == 4:
        # return cart items
        state = CART
        _, response = get_cart_items(message, user_state)

    elif message == 5:
        # return checkout message
        state = CHECKOUT
        _, response = get_checkout_view(message, user_state)
    elif message == 6:
        state = NOTIFICATIONS
        _, response = get_notifications_list(message, user_state)
    else:
        state, response = HOME, PARDON

    return state, response


def get_product_list(message, user_state):
    user_state["page"], response = get_products(user_state["page"], message)
    return False, response


def get_product_details(message, user_state):
    user_state["last_viewed_product"], response = get_product(int(message))
    return False, response


def get_order_list(message, user_state):
    user_state["page"], response = get_order_by_user(
        user_state["user_id"], user_state["page"], message
    )
    return False, response


def get_order_details(message, user_state):
    user_state["last_id"] = message
    return False, get_order_by_id(message, user_state["user_id"])


def add_to_cart(message, user_state):
    quantity = int(message.split(" ")[-1])
    response = user_state["cart"].add_product(
        user_state["last_viewed_product"], quantity
    )
    return False, response


def get_cart_items(message, user_state):
    response = user_state["cart"].get_cart_items()
    if response == "":
        return False, NO_MORE_ITEMS
    return False, response + REMOVE_FROM_CART + UPDATE_PRODUCT_IN_CART


def update_cart_item(message, user_state):
    message_args = message.split(" ")
    product_id = int(message_args[1])
    quantity = int(message_args[2])
    cart_response = user_state["cart"].update_product(product_id, quantity)
    _, response = get_home_response(4, user_state)
    return False, cart_response + response


def remove_cart_item(message, user_state):
    product_id = int(message.split(" ")[-1])
    user_state["cart"].remove_product(product_id)
    _, response = get_home_response(4, user_state)
    return False, response


def get_notifications_list(message, user_state):
    user_state["page"], response = get_latest_notifications_for_the_user(
        user_state["user_id"], user_state["page"], message
    )
    return False, response


def get_checkout_view(message, user_state):
    if user_state["cart"].total_cost() < MINIMUM_ORDER_VALUE:
        return True, user_state["cart"].get_cart_items() + MINIMUM_ORDER_VALUE_ERROR

    return (
        False,
        user_state["cart"].get_cart_items()
        + user_state["cart"].get_total_cost()
        + PROCEED,
    )


def get_shipping_address_message(message, user_state):
    print("Im in get_shipping")
    return (
        False,
        """
    Please enter shipping address.
    """,
    )


def udpate_shipping_address(message, user_state):
    user_state["shipping_address"] = message
    return False, PROCEED


def get_available_payment_methods(message, user_state):
    return False, get_payment_methods()


def set_payment_method(message, user_state):
    response = user_state["cart"].set_payment_method(message)
    if response == INVALID_ID:
        return True, INVALID_ID
    return False, response


def get_available_shipping_methods(message, user_state):
    response = get_shipping_methods()
    return False, response


def set_shipping_method_for_user(message, user_state):
    response = user_state["cart"].set_shipping_method(message)
    if response == INVALID_ID:
        return True, INVALID_ID
    return False, response


def get_refund_address_message(message, user_state):
    return (
        False,
        """
    Please enter refund address.
    """,
    )


def set_refund_address(message, user_state):
    user_state["cart"].set_refund_address(message)
    return False, PROCEED


def create_new_order(message, user_state):
    response = user_state["cart"].create_order(user_state["user_id"])
    return False, response


def get_create_ticket_confirm_message(message, user_state):
    return False, CREATE_TICKET_CONFIRM.format(user_state["last_id"])


def select_item_from_order_items(message, user_state):
    response = get_items_by_order_id(
        user_state["last_id"], user_state["user_id"]
    )
    return False, response


def get_ticket_subject_message(message, user_state):
    user_state["item_id"] = message
    return False, """
    Please type ticket subject
    """


def set_ticket_subject(message, user_state):
    user_state["ticket_subject"] = message
    return False, """
    Please type ticket message
    """


def set_ticket_message(message, user_state):
    user_state["ticket_message"] = message
    response = create_ticket_for_the_order(
        user_state["user_id"], user_state["item_id"],
        user_state["ticket_subject"], user_state["ticket_message"])
    return False, response
