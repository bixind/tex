n, m = map(int, input().split())

alpha = input().split()

f = set( map(int, input().split()) )

mt = dict()

for i in range(n):
    mt[i] = dict()
    for c in alpha:
        mt[i][c] = list()
    
for i in range(m):
    a, b, c = input().split()
    mt[int(a)][c].append(int(b))
    
och = [{0}]

cnt = 1
nmt = {0: dict()}
for a in alpha:
    nmt[0][a] = list()
    
label = {(0,) : 0}

while len(och) > 0:
    v = och.pop()
    lv = label[tuple(v)]
    for c in alpha:
        cur = set()
        for u in v:
            for w in mt[u][c]:
                cur.add(w)
        if tuple(sorted(cur)) not in label:
            nmt[cnt] = dict()
            for a in alpha:
                nmt[cnt][a] = list()
            label[tuple(sorted(cur))] = cnt
            cnt+=1;
            och.append(list(sorted(cur)))
        nmt[lv][c].append(label[tuple(sorted(cur))])

fancy = False

nf = set()

for pr in sorted(list(reversed(p)) for p in label.items()):
    if (len(list(filter(lambda x: x in f, pr[1])))):
        nf.add(pr[0])

if fancy:
    for pr in sorted(list(reversed(p)) for p in label.items()):
        if (len(list(filter(lambda x: x in f, pr[1])))):
            print(pr[0], pr[1], 'finish')
        else:
            print(pr[0], pr[1])
        for it in nmt[pr[0]].items():
            print("   ", it[0], it[1])
else:
    print(alpha)
    print(nf)
    print(nmt)
        
