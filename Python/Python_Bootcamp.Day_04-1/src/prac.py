import altair

from random import randint


def gen():
    i = 0
    step = 11
    while i < 100:
        x = yield i
        i += step
        if x != None:
            i += 1
            # print(i)


g = gen()
for i in g:
    print(i)
    if i > 30:
        g.send(1)
        continue
        print(i)

    # else:

# print(randint(0, 10))
