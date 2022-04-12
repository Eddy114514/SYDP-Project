

flist = [lambda x:x, lambda x:x]
f = lambda x: (flist[0](x)*flist[1](x))


print(f(2))
