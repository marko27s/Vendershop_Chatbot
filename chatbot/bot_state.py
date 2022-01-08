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

    ORDER_DETAILS: {
        MessageType.id_regex: {
            "next_node": TICKET_CREATED,
            "handler": get_create_ticket_confirm_message
        }
    },

    TICKET_CREATED: {
        MessageType.yes_regex: {
            "next_node": CREATE_TICKET_CONFIRM,
            "handler": select_item_from_order_items
        }
    },

    CREATE_TICKET_CONFIRM: {
        MessageType.id_regex: {
            "next_node": GET_TICKET_SUBJECT,
            "handler": get_ticket_subject_message
        }
    },

    GET_TICKET_SUBJECT: {
        MessageType.text_regex: {
            "next_node": SET_TICKET_SUBJECT,
            "handler": set_ticket_subject
        }
    },


    SET_TICKET_SUBJECT: {
        MessageType.text_regex: {
            "next_node": SET_TICKET_MESSAGE,
            "handler": set_ticket_message
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
    },

    TICKETS: {
        MessageType.next_regex: {
            "next_node": TICKETS,
            "handler": get_tickets_list
        },
        MessageType.back_regex: {
            "next_node": TICKETS,
            "handler": get_tickets_list
        },
        MessageType.id_regex: {
            "next_node": TICKET_DETAILS,
            "handler": get_ticket_details
        }
    },

    TICKET_DETAILS: {
        MessageType.text_regex: {
            "next_node": TICKET_DETAILS,
            "handler": send_new_message
        }
    }
}
