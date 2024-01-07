from calendar import c
import re
from flask import Flask,redirect, render_template,url_for,request


app = Flask(__name__, template_folder="./website/templates",static_folder="./website/static")

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("user", username=request.form["name"]))
    return render_template("login.html")


@app.route("/user/<username>")
def user(username):
    return f"Hello {username}"


if __name__ == "__main__":
    app.run(debug=True)
