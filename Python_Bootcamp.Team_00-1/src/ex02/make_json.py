import json

dic = {'1': ['2', '3'], '2': '3', '3': ['1', '2', '4']}

with open('../rel.yml', 'w') as f:
    f.write(json.dumps(dic))

s: set = set()
for i in dic:
    s.add(i)
    if isinstance(dic[i], list) or isinstance(dic[i], tuple):
        for j in dic[i]:
            s.add(j)
    else:
        s.add(dic[i])

x: dict = {}
for i in [*s]:
    x[i] = 1
for i in dic:
    if isinstance(dic[i], list) or isinstance(dic[i], tuple):
        for j in dic[i]:
            x[j] += 1
            print(j, '-')
    else:
        x[dic[i]] += 1
        print(dic[i])

for i in s:
    print(i, end=',')


print(s)
print(x)
