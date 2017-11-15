from flask import g, request, Response
from time import time
import flask
import json
#Some API utils. Used to return a proper HTTP Response

def ok(data):
    res = Response(data.to_json(), status=200, mimetype="application/json")
    add_cors_header(res)
    return res

def redirect(url, status_code=302):
    return flask.redirect(url, code=status_code)

def success():
    res = Response("{\"success\":true}", status=200, mimetype="application/json")
    add_cors_header(res)
    return res

def error(reason, errno):
    res = Response("{\"reason\":\"" + reason + "\"}", status=errno, mimetype="application/json")
    add_cors_header(res)
    return res

def add_cors_header(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Keep-Alive,User-Agent,\
                X-Requested-With,If-Modified-Since,Cache-Control,Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE,\
                                                        PUT, OPTIONS, PATCH'


    if 'HTTP_ORIGIN' in request.environ and ("localhost" in request.environ['HTTP_ORIGIN'] in request.environ['HTTP_ORIGIN']):
        response.headers['Access-Control-Allow-Origin'] = request.environ['HTTP_ORIGIN']
    else:
        response.headers['Access-Control-Allow-Origin'] = 'http://polyakov.student.utwente.nl'
    return response

def calculate_time():
    g.request_start_time = time()
    g.request_time = lambda: "%.3fms" % ((time() - g.request_start_time) * 1000)

def add_time_header(response):
    response.headers['X-Response-Time'] = g.request_time()
    return response;

def send_json(data):
    res = Response(json.dumps(data), status=200, mimetype="application/json")
    return add_cors_header(res)
