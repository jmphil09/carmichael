import numpy as np
from util import primesfrom2to

import time
start_time = time.perf_counter()

LARGE_PRIMES = primesfrom2to(10000000)


def is_prime(n):
    global LARGE_PRIMES
    if n > LARGE_PRIMES[-1]:
        LARGE_PRIMES = primesfrom2to(LARGE_PRIMES[-1] * 10)
        return is_prime(n)
    else:
        return n in LARGE_PRIMES


def calc_3_carms_for_p(current_prime, next_prime, thread_num):
    m = current_prime
    diff = next_prime - current_prime
    k = diff

    for B in range(2, m):
        a = int(np.floor((np.power(m, 2) / B)) + 1)
        b = int(np.floor((1 / B) * (np.power(m, 2) + ((m + B) * (m - 1)) / (m + k - 1))))

        for A in range(a, b + 1):
            p = 1 + ((m + B) * (m - 1)) / (A * B - np.power(m, 2))
            q = (A * (p-1) + 1) / m
            if np.floor(p) == p and np.floor(q) == q:  # np.floor(q) == q may not be needed
                if is_prime(p) and is_prime(q):
                    x = (p * q - 1) / (m - 1)
                    y = (m * q - 1) / (p - 1)
                    z = (m * p - 1) / (q - 1)
                    if np.floor(x) == x and np.floor(y) == y and np.floor(z) == z:
                        p1 = m
                        p2 = int(p)
                        p3 = int(q)
                        carm_num = p1*p2*p3
                        print((p1, p2, p3, carm_num))


def calc_3carm(limit):
    new_limit = limit
    while not is_prime(new_limit):
        new_limit += 1
    primes = primesfrom2to(new_limit + 1)

    for n in range(1, len(primes) - 1):
        current_prime = primes[n]
        m = current_prime
        next_prime = primes[n + 1]
        diff = next_prime - current_prime
        k = diff

        for B in range(2, m):
            a = int(np.floor((np.power(m, 2) / B)) + 1)
            b = int(np.floor((1 / B) * (np.power(m, 2) + ((m + B)*(m - 1)) / (m + k - 1))))

            for A in range(a, b + 1):
                p = 1 + ((m + B) * (m - 1)) / (A * B - np.power(m, 2))
                q = (A * (p-1) + 1) / m
                if np.floor(p) == p and np.floor(q) == q:  # np.floor(q) == q may not be needed
                    if is_prime(p) and is_prime(q):
                        x = (p * q - 1) / (m - 1)
                        y = (m * q - 1) / (p - 1)
                        z = (m * p - 1) / (q - 1)
                        if np.floor(x) == x and np.floor(y) == y and np.floor(z) == z:
                            p1 = m
                            p2 = int(p)
                            p3 = int(q)
                            carm_num = p1*p2*p3
                            print((p1, p2, p3, carm_num))


calc_3carm(101)
calc_3_carms_for_p(347, 349, 0)

end_time = time.perf_counter()
print('Run time: {} seconds'.format(end_time - start_time))
