from vendorshop.admin.models import Notification
from vendorshop.product.models import Product

from chatbot.bot_state import BOT_STATE
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
        self.user_state = {}

    def set_state_home(self) -> None:
        self.state = HOME
        self.page = 1

    def get_response(self, message) -> str:
        try:
            print("message", message)

            # identify input message type
            message_type, message = self.get_message_type(message)
            print("tesing", message_type, message)

            if self.state == HOME:
                self.state, response = BOT_STATE[self.state][message_type][RESPONSE](
                    message, self.user_state
                )

            else:
                self.state = BOT_STATE[self.state][message_type][NEXT_STATE]
                response = BOT_STATE[self.state][message_type][RESPONSE](
                    message, self.user_state
                )

            return response

        except Exception as e:
            print("ERROR", e)
        return PARDON

    def get_message_type(self, message):
        if message.isnumeric():
            return ID, int(message)
        elif message == "next":
            return NEXT, message
        elif message == "back":
            return BACK, message
        elif message.startswith("add"):
            return ADD, message
        elif message == "hone":
            return ID, int(message)
        return "", PARDON
