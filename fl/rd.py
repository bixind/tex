import ast
import itertools

alpha = ast.literal_eval(input())
f = ast.literal_eval(input())
mt = ast.literal_eval(input())

old_classes = [tuple(f), tuple(filter(lambda x: x not in f, mt))]

clnum = dict()
def repos():
    for i in range(len(old_classes)):
        for c in old_classes[i]:
            clnum[c] = i
repos()

old_cnt = 2

while True:
    res = dict()
    clsig = set()
    for st in mt:
        rch = list()
        for c in alpha:
            rch.append(clnum[mt[st][c][0]])
        res[st] = (clnum[st], tuple(rch))
        clsig.add((clnum[st], tuple(rch)))
    #print(len(clsig), clsig)
    if len(clsig) <= old_cnt:
        break
    g = dict()
    i = 0
    for sig in clsig:
        g[sig] = i;
        i += 1
    for st in mt:
        clnum[st] = g[res[st]]
    old_cnt = len(clsig)
        
print(old_cnt)

nf = set(map(lambda x: clnum[x], f))

nmt = dict()
for i in range(old_cnt):
    nmt[i] = dict()

for st in mt:
    for c in alpha:
        nmt[clnum[st]][c] = clnum[mt[st][c][0]]

for st in nmt:
    print(st, 'finish' if st in nf else '', 'start' if clnum[0] == st else '')
    for c in alpha:
        print('    ', c, nmt[st][c])
