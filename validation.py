import os
import time

missing = []

"""
Checks if there are any missing blocks in the primes directory, and returns a
list of the missing block numbers.
    start: the block from which the function should validate
"""
def validate(start):
    names = os.popen("ls /var/www/html/primes | sort -V").read().strip().split("\n")

    blocks = []

    for name in names:
        try:
            block = int(name.split('_')[1])
            block_size = int(name.split('_')[2].replace(".txt", ''))
        except IndexError:
            print("Unrecognized filename, continueing...")
            continue

        blocks.append([block, block_size])


    i = 0
    for block in blocks:
        if i < len(blocks) - 1:
            if blocks[i + 1][0] != block[0] + block[1]:
                # print("miss!", block, blocks[i + 1])
                check_block_num = block[0] + block[1]
                # zolang we nog niet bij het goede block zijn...
                while check_block_num != blocks[i + 1][0]:
                    if check_block_num not in missing:
                        missing.append(check_block_num)
                    check_block_num += block[1]

        i += 1

    return missing

def validation_loop():
    while True:
        prev_len = len(missing)

        validate(1600000000000000)
        time.sleep(60 * 60)

        if len(missing) != prev_len:
            print("Validated. Number of incorrect blocks: ", len(missing))
