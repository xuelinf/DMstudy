#coding: utf-8
__author__ = 'xuelinf'

n = 3
cin = [1, 4, 1]

res = [[],[],[],[]]

for i, e in enumerate(cin):
    res[e-1].append(i)

step = 0
dia = 0
flag = 0
while (dia < n):
    for i in range(4):
        if len(res[i]) > 0:
            if res[i][0] == dia:
                if i != flag:
                    step += 1
                    flag = i
                dia += 1
                res[i].remove(res[i][0])
print step