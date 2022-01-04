from chatbot.db_helper import *
from constants import *


def get_home_response(message, user_state):

    print("in get home response", message, user_state)
    print(type(message))
    if message == 1:
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
