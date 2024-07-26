import sys
from itertools import zip_longest

x: int = 0
for i, line in zip_longest(range(3), sys.stdin, fillvalue=3):
    if (i < 3 and len(line.strip('\n')) != 5):
        x = 2
        break
    if (i == 0):
        if (line[0] != '*' or line[1] == '*' or line[2] == '*' or line[3] == '*' or line[4] != '*'):
            x = 1
    elif (i == 1):
        if (line[0] != '*' or line[1] != '*' or line[2] == '*' or line[3] != '*' or line[4] != '*'):
            x = 1
    elif (i == 2):
        if (line[0] != '*' or line[1] == '*' or line[2] != '*' or line[3] == '*' or line[4] != '*'):
            x = 1
    else:
        if (line.strip('\n') != ""):
            x = 2

if (x == 0):
    print("True")
if (x == 1):
    print("False")
if (x == 2):
    print("Error")
