from calendar import c
import re
import sys
import json
from flask import Flask, Request,redirect, render_template,url_for
import requests



app = Flask(__name__, template_folder="./website/templates",static_folder="./website/static")
app.config['SECRET_KEY'] = 'oh_so_secret'

@app.route("/")
def home():
    return render_template("base.html")

from website.document_search import document_search_bp
app.register_blueprint(document_search_bp)

@app.route("/journal", methods=["POST", "GET"])
def wos_journal():
    
    return render_template("base.html")


#testing
"""
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("user", username=request.form["name"]))
    return render_template("login.html")


@app.route("/user/<username>")
def user(username):
    return f"Hello {username}"

"""
if __name__ == "__main__":
    app.run(debug=True)
