with open("in.txt") as f:
    a = f.readline()
    b = f.readline()
a = a.strip().split(",")
b = b.strip().split(",")
e = list(zip(a, b))
print(*e)
c = dict(zip(a, b))
d = list()
for i in c:
    t = int(i)
    d.append(t * int(c.get(i)))
print(*d)
f = list()
g = list()
for i, k in e:
    f.append(int(i))
    g.append(int(k))
h = 1
for i in f:
    h = h * i
print(h)
h = 1
for i in g:
    h = h * i
print(h)