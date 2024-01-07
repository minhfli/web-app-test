from flask import Blueprint

auth = Blueprint("view", __name__)

auth.route("/login")

def login():
    return "<h1>Login</h1>"

def logout():
    return "<h1>Logout</h1>"