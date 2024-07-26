import sys

amount: int = int(sys.argv[1])
line: str
for i, line in zip(range(amount), sys.stdin):
    line = line.strip('\n')
    if (len(line) == 32 and line[0:5] == "00000" and line[5] != '0'):
        print(line)
