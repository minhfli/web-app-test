from calendar import c
import sys
from flask import Flask,redirect, render_template,url_for,request


app = Flask(__name__, template_folder="./website/templates",static_folder="./website/static")

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/document", methods=["POST", "GET"])
def wos_document():
    if request.method == "POST":
        if request.form.get('Search') == 'Search':
            print("hello", file=sys.stderr)
    return render_template("wos_document.html")



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
