from calendar import c
import re
from tkinter import N
from unittest import result
from flask import Blueprint, redirect,render_template,Request,session,request, url_for
import json
import requests
from .api_data import APIKEY

document_search_bp = Blueprint('document_search', __name__, template_folder='templates')


def save_document_request(request:Request):
    json_data = request.form.to_dict(flat=True)
    session["d_form"] = json_data
    
@document_search_bp.route("/document", methods=["POST", "GET"])
def wos_document():
    clear_form = False
    if request.method == "POST":
        if request.form['action'] == "Search":
            save_document_request(request)
            session["submited"] = True
            #initial_json = get_json_request(session["d_form"])
            initial_json = None
            if initial_json is None:
                session.pop("d_results",None)
            else:
                session["d_results"] = initial_json
            return redirect("/document")
        elif request.form['action'] == "Clear":
            save_document_request(request)
            session["submited"] = False
            clear_form = True

    return render_template("wos_document.html",clear_form=clear_form,
                           results=json.dumps(session["d_form"])+ f'{session["submited"]}',session=session)
    if "d_results" in session:
        return render_template("wos_document.html",clear_form=clear_form,results= get_search_output(session["d_results"]))
    return render_template("wos_document.html",clear_form=clear_form,results="No document found")

#-----------------Helper functions-----------------
def get_json_request(input):
    if "OG" not in input:
        return None
    OG=input["OG"]
    if (OG==""):
        return None

    initial_request = requests.get(f'https://api.clarivate.com/apis/wos-starter/v1/documents?'
                               f'q=OG={input["OG"]}'
                               f'&limit=50&page=1&db=WOS&sortField=PY+D', headers={'X-ApiKey': APIKEY})
    initial_json = initial_request.json()
    return initial_json

def get_search_output(initial_json):
    if "hits" not in initial_json:
        if "message" in initial_json:
            return initial_json["message"]
        return "No document found"
    
    font_tag = '<p style="font-family:\'Source Sans Pro\'; line-height: 0.5">'
    output = f'{font_tag}Most Recent Documents :<br><br></p>'
    
    for i, record in enumerate(initial_json['hits'][:10]):
        authors = create_authors_list(record)
        title = format_title_length(record)

        output += (f'{font_tag}{i + 1}:  Title: <a href={record["links"]["record"]}>'
                   f'{title}</a><br></p>')
        output += f'{font_tag}    By: {authors}<br>'
        output += (f'{font_tag}    Published in: {record["source"]["sourceTitle"]}'
                   f'<br><br></p>')
    return output

def create_authors_list(doc):
    authors = []
    for author in doc['names']['authors']:
        if 'researcherId' in author:
            profile_link = (f'https://www.webofscience.com/wos/author/record/'
                            f'{author["researcherId"]}')
            authors.append(f'<a href={profile_link}>{author["wosStandard"]}</a>')
        else:
            authors.append(author["wosStandard"])
    if len(doc['names']['authors']) < 4:
        return ', '.join(authors)
    return f"{', '.join(authors[:3])} et al."


def format_title_length(doc):
    if len(doc['title']) > 100:
        return f"{doc['title'][:100]}..."
    return doc['title']
