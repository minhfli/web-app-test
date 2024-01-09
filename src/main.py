from calendar import c
import re
import sys
import json
from flask import Flask, Request,redirect, render_template,url_for,request,session
import requests



app = Flask(__name__, template_folder="./website/templates",static_folder="./website/static")
app.config['SECRET_KEY'] = 'oh_so_secret'

@app.route("/")
def home():
    return render_template("base.html")

def save_document_request(request:Request):
    json_data = request.form.to_dict(flat=True)
    session["d_form"] = json_data
    
@app.route("/document", methods=["POST", "GET"])
def wos_document():
    if request.method == "POST":
        if request.form['action'] == "Search":
            save_document_request(request)
        elif request.form['action'] == "Clear":
            save_document_request(request)
            return render_template("wos_document.html",clear_form=True,results=json.dumps(session["d_form"]))
        
            
    if "json" in session:
        return render_template("wos_document.html",clear_form=False,results=json.dumps(session["d_form"],))
    return render_template("wos_document.html",clear_form=True,results="No document request")

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
