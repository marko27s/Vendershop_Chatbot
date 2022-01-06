from chatbot.handlers import *
from constants import *

bob_state_graph = {
    
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
            "handler": get_products
        },
        MessageType.back_regex: {
            "next_node": SHOP, 
            "handler": get_products
        },
    },
    
    PRODUCT_DETAILS: {
        MessageType.add_regex: {
            "next_node": PRODUCT_DETAILS,
            "handler": add_to_cart
        }
     },

}