from flask import Blueprint, jsonify, request
from multiprocessing.connection import Client
from interface import IRequest, IPageResult
import uuid, zlib
from datetime import datetime, timedelta

NAME = "/tmp/work_socket"
c = Client(NAME, authkey=b"qwerty")

Api = Blueprint('Api', __name__)

@Api.route("/info")
def info(): 
    return  jsonify({"error": False, "result": ["hello", "world"] })


@Api.route("/start") 
def start():
    return jsonify({"error": False, "result": ["hello", "world"] })


@Api.route("/page", methods=["GET", "POST"]) 
def getpage():
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
            jscript = jscript if jscript else ""
        )
        c.send( param.__dict__ )
        data.append(param.id)
        # data.append( c.recv() )
        
    return jsonify({"response": True, "data" : data})


@Api.route("/result/<keyid>", methods=["GET", "POST"]) 
def get_result(keyid):
    data = []
    res = IPageResult(id=keyid)
    c.send( res.__dict__ )
    response = c.recv()
    if response:
        data.append( zlib.decompress( response ).decode("utf8") )
    return jsonify({"response": True, "data" : data})