import os

from flask import Flask, jsonify, redirect, render_template, request, session
from vendorshop import create_app
from vendorshop.extensions import db
from vendorshop.user.models import User

from chatbot.chatbot import ChatBot
from constants import PARDON, REQUEST_TO_LOGIN
from flask_session import Session

create_app().app_context().push()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE", "filesystem")
Session(app)


@app.route("/response", methods=["GET", "POST"])
def response():

    # get the message from user
    msg = request.form.get("msg")

    # if there is an active session then get response
    # from chatbot
    if session.get("chatbot") is not None:
        print("In Chatbot")
        return jsonify({
            "response": session.get("chatbot").get_response(msg.lower().strip())
        })
    elif msg.startswith("login"):
        username = msg.split(" ")[-1]
        if username != "":
            user = User.query.filter(User.username == username.strip()).first()
            if user is not None:
                print(f"{username}")
                session["chatbot"] = ChatBot(user)
                return jsonify({"response": session.get("chatbot").get_response("1")})
                # return jsonify(
                #     {"response": f"Welcome {session.get('chatbot').user.username}"}
                # )
    else:
        # request user to login via username
        return jsonify({"response": REQUEST_TO_LOGIN})

    # pardon! if input message is not in the context
    return jsonify({"response": PARDON})


@app.route("/chat")
def chat():
    """
    Main chat web page
    """
    return render_template("home.html")
