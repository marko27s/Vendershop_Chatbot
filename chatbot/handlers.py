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
        response = get_order_list(message, user_state)

    elif message == 4:
        # return cart items
        state = CART
        response = get_cart_items(message, user_state)
    else:
        response = PARDON

    return state, response


def get_product_list(message, user_state):
    user_state["page"], response = get_products(user_state["page"], message)
    return response


def get_product_details(message, user_state):
    user_state["last_viewed_product"], response = get_product(int(message))
    return response


def get_order_list(message, user_state):
    user_state["page"], response = get_order_by_user(
        user_state["user_id"], user_state["page"], message
    )
    return response


def add_to_cart(message, user_state):
    quantity = int(message.split(" ")[-1])
    response = user_state["cart"].add_product(
        user_state["last_viewed_product"], quantity
    )
    return response


def get_cart_items(message, user_state):
    response = user_state["cart"].get_cart_items()
    if response == "":
        return NO_MORE_ITEMS
    return response + REMOVE_FROM_CART + UPDATE_PRODUCT_IN_CART


def update_cart_item(message, user_state):
    message_args = message.split(" ")
    product_id = int(message_args[1])
    quantity = int(message_args[2])
    cart_response = user_state["cart"].update_product(product_id, quantity)
    _, response = get_home_response(4, user_state)
    return cart_response + response


def remove_cart_item(message, user_state):
    product_id = int(message.split(" ")[-1])
    user_state["cart"].remove_product(product_id)
    _, response = get_home_response(4, user_state)
    return response
