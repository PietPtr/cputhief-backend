from flask import Flask
from flask import request
from flask import jsonify
from flask import session, g, redirect, url_for, abort, render_template, flash
import api
import json
import threading
import validation
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'cputhief.db'),
        SECRET_KEY='geheimpje ;)',
        USERNAME='admin',
        PASSWORD='default'
    ))
app.config.from_envvar('CPUTHIEF_SETTINGS', silent=True)

from database import *

block_size = 1024

pointer = 0

val_thread = threading.Thread(target=validation.validation_loop)
val_thread.deamon = True
# val_thread.start()

with app.app_context():
    print("fetching pointer...")
    db = get_db()
    cur = db.execute('select max(blocknum) from blocks;')
    pointer = cur.fetchone()[0]
    print("starting at pointer", pointer, "...")

@app.route("/api/test", methods=['POST', 'GET'])
def test():
    db = get_db()
    cur = db.execute('select exists(select * from primes where number = 13);')
    entries = cur.fetchall()

    for e in entries:
        print (e[0])

    return api.success()

@app.route("/api/get_number", methods=['GET'])
def get_number():
    global pointer
    global block_size

    # if len(validation.missing) > 0:
    #     print(validation.missing)
    #     block = { "block": validation.missing[0], "n": block_size }
    #     validation.missing.pop(0)
    #     return api.send_json(block)

    block = { "block": pointer, "n": block_size }
    pointer += block_size
    return api.send_json(block)

@app.route("/api/post_results", methods = ['POST'])
def post_results():
    data = json.loads(request.data.decode())

    db = get_db()
    for prime in data["result"]:
        cur = db.execute('select exists(select * from primes where number = ?);', (prime,))
        if (cur.fetchall()[0][0]):
            db.execute('update primes set checked = checked + 1 where number = ?;', (prime,))
        else:
            db.execute('insert into primes values (?, 1)', (prime,))

    db.execute('insert into blocks values(?, ?)', (data["block"], data["n"]))

    db.commit()

    return api.success()

@app.route("/api/num_primes", methods = ['GET'])
def num_primes():
    amount = 0
    return api.succes()

@app.route("/api/validate", methods = ['POST'])
def validate():
    ip = os.popen("ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'").read().strip()

    if ip != request.remote_addr:
        return api.error("You're not me :)", 418)


    return api.success()

def start():
    global pointer

    print("fetching pointer...")
    db = get_db()
    cur = db.execute('select max(number) from primes;')
    pointer = cur.fetchone()
    print("starting at pointer", pointer, "...")
