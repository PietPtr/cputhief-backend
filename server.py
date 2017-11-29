from flask import Flask
from flask import request
import api
import json
import threading
import validation
import os

app = Flask(__name__)

block_size = 1024

pointer = int(os.popen("ls /var/www/html/primes | tail -n 1").read().split('_')[1])
print("starting at", pointer, "...")

primeFile = open("primes.dat", "wb")

val_thread = threading.Thread(target=validation.validation_loop)
val_thread.deamon = True
val_thread.start()

@app.route("/api/test", methods=['POST', 'GET'])
def test():
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

    primeFile = open("/var/www/html/primes/block_" + str(data["block"]) + \
                     "_" + str(block_size) + ".txt", "w")

    for prime in data["result"]:
        primeFile.write(str(prime) + "\n")

    return api.success()

@app.route("/api/num_primes", methods = ['GET'])
def num_primes():
    amount = 0
    return api.succes()
