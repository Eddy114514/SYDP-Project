def f(x):
    if (x < 0):
        return False
    save = x
    res = 0
    while (x > 0):
        res = x%10 + res*10
        x //= 10
    return True if save == res else False
print(f(121))