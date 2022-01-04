from chatbot.response import *
from constants import *

BOT_STATE = {
    HOME: {ID: {RESPONSE: get_home_response}},
    SHOP: {
        ID: {NEXT_STATE: PRODUCT_DETAILS, RESPONSE: get_product_details},
        NEXT: {NEXT_STATE: SHOP, RESPONSE: get_products},
        BACK: {NEXT_STATE: SHOP, RESPONSE: get_products},
    },
    PRODUCT_DETAILS: {ADD: {NEXT_STATE: ADD_TO_CART}},
}
