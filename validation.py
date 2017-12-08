"""
WARNING

Currently, validation does not trigger automatically. Occasionally make a post
request from the machine running the server to /api/validate to validate all
blocks.

curl --request POST localhost:5000/api/validate
"""

import os
import time
# from server import get_blocks
# from database import db
from flask import current_app
from database import *

missing = []


"""
Checks if there are any missing blocks in the primes directory, and returns a
list of the missing block numbers.
    start: the block from which the function should validate
"""
def validate():
    blocks = get_blocks()

    # check of blok gevolgd wordt door blocknum + block_size
        # zo niet: maak [block, block_size_tot_volgende] aan in missing

    i = 0
    for block in blocks[:len(blocks) - 1]:
        if block["blocknum"] + block["blocksize"] != blocks[i + 1]["blocknum"]:
            print(block["blocknum"])
            check_block_num = block["blocknum"] + block["blocksize"]
            while check_block_num != blocks[i + 1]["blocknum"]:
                missing_block = {"blocknum": check_block_num, "blocksize": block["blocksize"]}
                if missing_block not in missing:
                    missing.append(missing_block)
                check_block_num += block["blocksize"]

        i += 1



    print(missing)

def get_blocks():
    blocks = []
    with current_app.app_context():
        db = get_db()
        cur = db.execute('select * from blocks order by blocknum;')
        for block in cur.fetchall():
            blocks.append({"blocknum": block["blocknum"],
                           "blocksize": block["blocksize"]})

    return blocks

def validation_loop():
    while True:
        prev_len = len(missing)

        validate(get_blocks())
        time.sleep(60 * 60)

        if len(missing) != prev_len:
            print("Validated. Number of incorrect blocks: ", len(missing))
