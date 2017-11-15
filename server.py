from flask import Flask
from flask import request
import api

app = Flask(__name__)

@app.route("/api/test", methods=['POST', 'GET'])
def test():
    return api.success()

@app.route("/api/get_number", methods=['GET'])
def get_number():
    block = { "block": 0 }
    return api.send_json(block)
