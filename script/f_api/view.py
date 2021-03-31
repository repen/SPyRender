from flask import Blueprint, jsonify, request
from multiprocessing.connection import Client
from interface import IRequest, IPageResult
import uuid, zlib
from datetime import datetime, timedelta
from tool import log

l = log("Api")

NAME = "/tmp/work_socket"

Api = Blueprint('Api', __name__)

@Api.route("/info")
def info(): 
    return  jsonify({"error": False, "result": ["hello", "world"] })


@Api.route("/start") 
def start():
    return jsonify({"error": False, "result": ["hello", "world"] })


@Api.route("/render", methods=["GET", "POST"]) 
def render():
    data = []

    if request.form:
        url  = request.form.get("url")
        wait = request.form.get("wait")
        jscript = request.form.get("jscript")
        ctime =int( ( datetime.now() + timedelta(seconds=60*5) ).timestamp() )
        param = IRequest(
            id=uuid.uuid4().hex, 
            url=url, param={}, 
            wait=float(wait) if wait else 1,
            expiration_date = ctime,
            jscript = jscript if jscript else "",
            method = "render"
        )

        c = Client(NAME, authkey=b"qwerty")
        c.send( param.__dict__ )
        data.append(param.id)
        l.info(f"Request {param}")
        c.close()

        # data.append( c.recv() )
        
    return jsonify({"response": True, "data" : data})


@Api.route("/result/<keyid>", methods=["GET", "POST"]) 
def get_result(keyid):
    data = []
    res = IPageResult(id=keyid, method="result")
    c = Client(NAME, authkey=b"qwerty")
    c.send( res.__dict__ )
    response = c.recv()
    if response:
        l.info(f"Request {res}")
        data.append( zlib.decompress( response ).decode("utf8") )
    c.close()
    return jsonify({"response": True, "data" : data})


@Api.route("/a_content", methods=["POST"]) 
def active_content():
    data = []

    if request.form:

        wait    = request.form.get("wait")
        jscript = request.form.get("jscript")
        param = IRequest(
            id="", 
            url="", param={}, 
            wait=float(wait) if wait else 1,
            expiration_date = 0,
            jscript = jscript if jscript else "",
            method = "active_content"
        )
        c = Client(NAME, authkey=b"qwerty")
        c.send( param.__dict__ )
        '''Здесь часто происходит ошибка'''
        response = c.recv()
        if response:
            data.append( response )
            l.info(f"Request {param}")
        c.close()

    return jsonify({"response": True, "data" : data})

