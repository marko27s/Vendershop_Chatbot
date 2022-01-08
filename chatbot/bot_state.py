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
            "handler": get_order_details
        }
    },

    NOTIFICATIONS: {
        MessageType.next_regex: {
            "next_node": NOTIFICATIONS,
            "handler": get_notifications_list
        },
        MessageType.back_regex: {
            "next_node": NOTIFICATIONS,
            "handler": get_notifications_list
        }
    },

    CHECKOUT: {
        MessageType.next_regex: {
            "next_node": SHIPPING_ADDRESS,
            "handler": get_shipping_address_message
        }
    },

    SHIPPING_ADDRESS: {
        MessageType.text_regex: {
            "next_node": SHIPPING_ADDRESS_SET,
            "handler": udpate_shipping_address
        }
    },

    SHIPPING_ADDRESS_SET: {
        MessageType.next_regex: {
            "next_node": PAYMENT_METHOD,
            "handler": get_available_payment_methods
        }
    },

    PAYMENT_METHOD: {
       MessageType.id_regex: {
            "next_node": PAYMENT_METHOD_SET,
            "handler": set_payment_method
       }
    },

    PAYMENT_METHOD_SET: {
        MessageType.next_regex: {
            "next_node": SHIPPING_METHOD,
            "handler": get_available_shipping_methods
        }
    },

    SHIPPING_METHOD: {
        MessageType.id_regex: {
            "next_node": SHIPPING_METHOD_SET,
            "handler": set_shipping_method_for_user
        }
    },

    SHIPPING_METHOD_SET: {
        MessageType.next_regex: {
            "next_node": REFUND_ADDRESS,
            "handler": get_refund_address_message
        }
    },

    REFUND_ADDRESS: {
        MessageType.text_regex: {
            "next_node": REFUND_ADDRESS_SET,
            "handler": set_refund_address
        }
    },

    REFUND_ADDRESS_SET: {
        MessageType.next_regex: {
            "next_node": ORDER_CREATED,
            "handler": create_new_order
        }
    }
}
