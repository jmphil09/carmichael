import numpy

from math import gcd


# TODO: Replace this with a faster version.
def is_carm(n):
    """Check if n is a Carmichael number."""
    for b in range(2, n):
        if gcd(b, n) == 1:
            if pow(b, n-1, n) != 1:
                return False
    return True


# Consider replacing this with a better version at some point.
def primesfrom2to(n):
    """Input n>=6, Returns list of primes, 2 <= p < n ."""
    sieve = numpy.ones(n//3 + (n % 6 == 2), dtype=numpy.bool)
    for i in range(1, int(n**0.5)//3+1):
        if sieve[i]:
            k = 3*i+1 | 1
            sieve[k*k//3::2*k] = False
            sieve[k*(k-2*(i & 1)+4)//3::2*k] = False
    return [ numpy.int64(num) for num in numpy.r_[2, 3, ((3*numpy.nonzero(sieve)[0][1:]+1) | 1)]]


def is_prime(n, prime_limit=1000000):
    large_primes = primesfrom2to(prime_limit)
    if n > large_primes[-1]:
        return is_prime(n, prime_limit*10)
    else:
        return n in large_primes
