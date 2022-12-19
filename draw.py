import time
from random import random


def norm(mean=0, std=1):
    size = int(1e3)
    value = sum([(random() - 0.5) * 100 for _ in range(size)])
    return (value / size) * std + mean


def block_str(e, canvas_size):
    block = ""
    for i in range(canvas_size[0] * canvas_size[1]):
        if i != 0 and (i % canvas_size[0]) == 0:
            block += "\n"
        if i < e:
            block += "*"
        else:
            block += " "
    block += "\n"
    return block


def render(scr, vals):
    scr.erase()

    blocks = ""

    for val in vals:
        blocks += f"{val[1]}:\n" + block_str(val[0], (5, 5))

    for y, line in enumerate(blocks.split("\n")):
        scr.addstr(y, 0, line)

    scr.refresh()


def main(scr):
    a = 10
    b = 15

    for i in range(10):

        changes = round(norm(std=2))
        while changes >= a or -changes >= b:
            changes = round(norm(std=2))

        a -= changes
        b += changes


        time.sleep(1)
    scr.getkey()
