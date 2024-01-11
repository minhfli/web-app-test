from calendar import c
import re
from tkinter import N
from unittest import result
from flask import Blueprint, redirect,render_template,Request,session,request, url_for
import json
import requests
from sqlalchemy import false
from .api_data import APIKEY

document_search_bp = Blueprint('document_search', __name__, template_folder='templates')
clarivate_json = requests.get(f'https://api.clarivate.com/apis/wos-starter/v1/documents?'
                               f'q=OG=Clarivate'
                              f'&limit=50&page=1&db=WOK&sortField=PY+D', headers={'X-ApiKey': APIKEY}).json()

def save_document_request(request:Request):
    session.pop("d_form",None)
    json_data = request.form.to_dict(flat=True)
    session["d_form"] = json_data
    
@document_search_bp.route("/document", methods=["POST", "GET"])
def wos_document():
    clear_form = False
    if request.method == "POST":
        if request.form['action'] == "Search":
            save_document_request(request)
            session.pop("d_results",None)
            initial_json = None #for testing
            initial_json = get_json_request(query_builder(session["d_form"]))            
            if initial_json is not None:
                session["d_results"] = initial_json
            return redirect("/document")
        elif request.form['action'] == "Clear":
            session.pop("d_form",None)

    #return render_template("wos_document.html",clear_form=clear_form,session=session,results=query_builder(session["d_form"]))   
    #return render_template("wos_document.html",clear_form=clear_form,session=session,results=get_search_output(clarivate_json))
    #return render_template("wos_document.html",clear_form=clear_form,session=session,results=json.dumps(clarivate_json))
    if "d_results" in session:
        return render_template("wos_document.html",clear_form=clear_form,results= get_search_output(session["d_results"]),session=session)
    return render_template("wos_document.html",clear_form=clear_form,results="No document found",session=session)

#-----------------Helper functions-----------------
def get_json_request(query):
    if query is None:
        return None
    
    initial_request = requests.get(query, headers={'X-ApiKey': APIKEY}).json()
    return initial_request

def add_to_query(q,key,value,first_attribute):
    if value is None or value == '':
        return q,first_attribute
    if first_attribute:
        q+= f' AND {key}={value}'
    else:
        q += f'{key}={value}'
        first_attribute = True
    return q,first_attribute
def query_builder(input):
    if 'd_form' not in session:
        return None

    if input['UID'] is not None and input['UID'] != '':
        return f'https://api.clarivate.com/apis/wos-starter/v1/documents/uid?'\
        f'db=WOK&'\
        f'uid={input["UID"]}'\
        f'&limit=50&page=1&sortField=RS+D'
    
    first_attribute = False

    query = ''
    query,first_attribute = add_to_query(query,'TI',input['TI'],first_attribute)
    query,first_attribute = add_to_query(query,'IS',input['IS'],first_attribute)
    query,first_attribute = add_to_query(query,'SO',input['SO'],first_attribute)
    query,first_attribute = add_to_query(query,'VL',input['VL'],first_attribute)
    query,first_attribute = add_to_query(query,'CS',input['CS'],first_attribute)
    query,first_attribute = add_to_query(query,'PY',input['PY'],first_attribute)
    query,first_attribute = add_to_query(query,'AU',input['AU'],first_attribute)
    query,first_attribute = add_to_query(query,'AI',input['AI'],first_attribute)
    query,first_attribute = add_to_query(query,'UT',input['UT'],first_attribute)
    query,first_attribute = add_to_query(query,'DO',input['DO'],first_attribute)
    query,first_attribute = add_to_query(query,'DT',input['DT'],first_attribute)
    query,first_attribute = add_to_query(query,'PMID',input['PMID'],first_attribute)
    query,first_attribute = add_to_query(query,'OG',input['OG'],first_attribute)
    query,first_attribute = add_to_query(query,'TS',input['TS'],first_attribute)
    
    if not first_attribute:
        return None    
    return f'https://api.clarivate.com/apis/wos-starter/v1/documents?'\
        f'db=WOK&'\
        f'q=({query})'\
        f'&limit=50&page=1&sortField=RS+D' 

def get_search_output(initial_json):
    if "hits" not in initial_json:
        if "message" in initial_json:
            return initial_json["message"]
        return "No document found"
    
    font_tag = '<p style="font-family:\'Source Sans Pro\'; line-height: 0.5">'
    output = f'{font_tag}Most Recent Documents :<br><br></p>'
    
    for i, record in enumerate(initial_json['hits'][:2]):
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
    if len(doc['names']['authors']) < 6:
        return ', '.join(authors)
    return f"{', '.join(authors[:5])} et al."


def format_title_length(doc):
    if len(doc['title']) > 100:
        return f"{doc['title'][:100]}..."
    return doc['title']
