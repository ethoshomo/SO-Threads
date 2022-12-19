from random import random


def norm(mean=0, std=1):
    size = int(1e3)
    value = sum([(random() - 0.5) * 100 for _ in range(size)])
    return (value / size) * std + mean


def block_str(e, total, canvas_size):
    block = ""
    for i in range(canvas_size[0] * canvas_size[1]):
        if i != 0 and (i % canvas_size[0]) == 0:
            block += "\n"
        if i < e:
            block += "*"
        elif i < total:
            block += "."
        else:
            block += " "
    block += "\n"
    return block


def make_block(val):
    return f"{val[2]}:\n" + block_str(val[0], val[1], (7, int(val[0] / 7) + 2))


def render(scr, vals):
    scr.erase()

    blocks = "******************* POSTO DE COMBUSTIVEL *******************\n"

    for val in vals:
        blocks += f"{val[2]}:\n" + block_str(val[0], val[1], (7, int(val[0] / 7) + 2))

    for y, line in enumerate(blocks.split("\n")):
        scr.addstr(y, 0, line)

    scr.refresh()
