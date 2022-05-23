a = [lambda x: 2*x, lambda x:x*3, lambda x: x]
b = [lambda x: 2*x, lambda x:x*3, lambda x: x]
c = []
for j, k in zip(a, b):
    c.append(lambda x: j(x)*k(x))

for i in c:
    print(i(2))
