from chatbot.db_helper import *
from constants import *


def get_home_response(message, user_state):

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
        user_state["page"] = 1
        user_state["page"], response = get_products(user_state["page"], "")
    else:
        response = PARDON

    return state, response


def get_product_list(message, user_state):
    user_state["page"] = 1
    user_state["page"], response = get_products(user_state["page"], message)
    return response


def get_product_details(message, user_state):
    user_state["last_viewed_product"], response = get_product(int(message))
    return response


def add_to_cart(message, user_state):
    quantity = int(message.split(" ")[-1])
    response = user_state["cart"].add_product(
        user_state["last_viewed_product"], quantity
    )
    return response
