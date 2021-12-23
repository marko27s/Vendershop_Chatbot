from flask import Flask, jsonify, redirect, render_template, request, session

from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/response", methods=["GET", "POST"])
def response():
    print(request.json)
    print(request.form)
    msg = request.form.get("msg")
    if msg.startswith("/login"):
        username = msg.split(" ")[-1]
        session["username"] = username
        return jsonify({"response": f"Welcome {username}"})

    if msg.startswith("/name"):
        return jsonify({"response": f"Welcome {session['username']}"})

    return jsonify({"response": f"Pardon!, Can you please ask again?"})


@app.route("/")
def index():
    return session.get("username", "")


@app.route("/chat")
def chat():
    return render_template("home.html")
