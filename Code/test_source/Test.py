import time


def prime_check(prime):
    for i in range(2, prime):
        if (prime % i == 0):
            return False
    return True


start = time.time()
i = 0
count = 0
while (i <= 10000):
    if prime_check(i):
        count += 1
    i += 1

print(f"the count of prime number is {count}")
end = time.time()
print("runtime: ", end - start)
