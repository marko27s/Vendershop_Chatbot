from chatbot.handlers import *
from constants import *

bot_state_graph = {
    
    HOME: {
        MessageType.id_regex: {
            "handler": get_home_response
        }
    },
    
    SHOP: {
        MessageType.id_regex: {
            "next_node": PRODUCT_DETAILS, 
            "handler": get_product_details
        },
        MessageType.next_regex: {
            "next_node": SHOP, 
            "handler": get_product_list
        },
        MessageType.back_regex: {
            "next_node": SHOP, 
            "handler": get_product_list
        },
    },
    
    PRODUCT_DETAILS: {
        MessageType.add_regex: {
            "next_node": PRODUCT_DETAILS,
            "handler": add_to_cart
        }
     },

    CART: {
        MessageType.update_regex: {
            "next_node": CART,
            "handler": update_cart_item
        },
        MessageType.remove_regex: {
            "next_node": CART,
            "handler": remove_cart_item
        }
    },

    ORDERS: {
        MessageType.next_regex: {
            "next_node": ORDERS,
            "handler": get_order_list
        },
        MessageType.back_regex: {
            "next_node": ORDERS,
            "handler": get_order_list
        },
        MessageType.id_regex: {
            "next_node": ORDER_DETAILS,
            "handler": get_order_by_id
        }
    }

}