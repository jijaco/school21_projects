from random import randint
from time import sleep


def valve(gen):
    if i > 80:
        gen.send(-1)
    elif i < 20:
        gen.send(1)


def emit_gel(step: float):
    pressure: float = step

    i = None
    t = 1
    while True:
        i = yield pressure
        t = i if i != None else t

        r_step = randint(0, step) * t
        pressure += r_step
        pressure = min(pressure, 100)
        if i != None:
            yield pressure
        sleep(1)


if __name__ == "__main__":
    max_step = 30
    gen = emit_gel(max_step)
    for i in gen:
        print(i)
        if i > 90 or i < 10:
            gen.close()
        else:
            valve(gen)
