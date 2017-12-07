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

block_size = 1024

pointer = int(os.popen("ls /var/www/html/primes | tail -n 1").read().split('_')[1])
print("Starting at", pointer, "...")

val_thread = threading.Thread(target=validation.validation_loop)
val_thread.deamon = True
val_thread.start()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('initialized the database')

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

    if len(validation.missing) > 0:
        print(validation.missing)
        block = { "block": validation.missing[0], "n": block_size }
        validation.missing.pop(0)
        return api.send_json(block)

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

    validation.validate(1600000000000000)
    print("Validated. Number of incorrect blocks: ", len(validation.missing))

    return api.success()
