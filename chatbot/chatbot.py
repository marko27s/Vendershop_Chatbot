import re

from vendorshop.admin.models import Notification
from vendorshop.product.models import Product

from chatbot.bot_state import bot_state_graph
from chatbot.cart import Cart
from chatbot.db_helper import *
from constants import *


class ChatBot:
    def __init__(self, user) -> None:

        # save logged in user
        self.user = user

        # set default state to home (main menu)
        self.current_node = HOME

        # for saving messages and responses
        self.conversation_meta = {}

        # for saving cart and other user related info
        self.user_state = {"cart": Cart(user.default_shipping_address)}

    def get_response(self, message) -> str:
        try:

            # identify input message regex
            matched_regex = self.get_matched_regex(message)

            # main menu options have high precedence, regardless of current node
            if self.current_node == HOME or message in MAIN_MENU_OPTIONS_LIST:
                self.current_node, response = bot_state_graph[HOME][matched_regex][
                    "handler"
                ](message, self.user_state)

            # get handler and next node based on current node
            # handler will return response based on the input message
            else:
                response = bot_state_graph[self.current_node][matched_regex]["handler"](
                    message, self.user_state
                )
                self.current_node = bot_state_graph[self.current_node][matched_regex][
                    "next_node"
                ]

            return response
        except Exception as e:
            print("ERROR", e)
            return PARDON

    def get_matched_regex(self, message):
        """
        input: message
        output: matched regex from available regexes based on current node
        """
        if message in MAIN_MENU_OPTIONS_LIST:
            return MessageType.id_regex

        for regex in bot_state_graph[self.current_node].keys():
            _regex = re.compile(r"{}".format(regex.value))
            matched = bool(_regex.match(message))
            if matched:
                print("Matched Regex: ", regex)
                return regex
        return None
