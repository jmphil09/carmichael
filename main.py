import numpy
import pickle
import random

from math import gcd
from multiprocessing import Pool

import time
start_time = time.perf_counter()

NUM_CORES = 16
PRIME_UPPER_BOUND = 1000


found_carm_set = set()


def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n//3 + (n%6==2), dtype=numpy.bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]


primes_to_check = primesfrom2to(PRIME_UPPER_BOUND)
random.shuffle(primes_to_check)
n = NUM_CORES - 1
n_list_size = int(len(primes_to_check)/NUM_CORES)
split_primes = [list(primes_to_check[i*n_list_size:(i+1)*n_list_size]) for i in range(0,n)] + [list(primes_to_check[(n)*n_list_size::])]


def is_carm(n):
    """ Check whether n is a Carmichael number """
    for b in range(2, n):
        # If b is relatively prime to n
        if gcd(b, n) == 1:
            # If pow(b, n-1) % n is not 1, not Carmichael
            if pow(b, n-1, n) != 1:
                return False
    return True


def generate_3carm(core_num, p1_primes):
    #print('core_num: {}'.format(core_num))
    #print('p1_primes: {}'.format(p1_primes))
    for p1 in p1_primes:
        for p2 in primes_to_check:
            for p3 in primes_to_check:
                if p1 < p2 and p2 < p3:
                    candidate = p1*p2*p3
                    if is_carm(int(candidate)):
                        existing_results = []
                        new_result = [(p1, p2, p3, p1*p2*p3)]
                        filename = 'found_carm_{}'.format(core_num)
                        try:
                            infile = open(filename,'rb')
                            existing_results = pickle.load(infile)
                            infile.close()
                            result = existing_results + new_result
                        except Exception as e:
                            result = new_result
                        outfile = open(filename, 'wb')
                        pickle.dump(result, outfile)
                        outfile.close()
                        #print('p1: {}, p2: {}, p3: {}, p1*p2*p3: {}'.format(p1, p2, p3, p1*p2*p3))


def run_all_threads():
    p = Pool(processes=NUM_CORES)
    #p.map(generate_3carm, tuple((i, split_primes[i]) for i in range(0, NUM_CORES)))
    #p.starmap(generate_3carm, [[1, [1,2,3]]])
    p.starmap(generate_3carm, [[i, split_primes[i]] for i in range(0, NUM_CORES)])

#generate_3carm(primes_to_check)
#print(sorted(list(found_carm_set)))
#[3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 61, 67, 73, 97]


if __name__ == '__main__':
    try:
        #filename = 'found_carm_{}'.format(1)
        #infile = open(filename,'rb')
        #new_dict = pickle.load(infile)
        #print(new_dict)
        #print(set(new_dict))
        #infile.close()
        pass
    except Exception as ex:
        pass
    #num_runs = 4
    #for i in range(num_runs):
    run_all_threads()
    #end_time = time.perf_counter()
    #print("{} runs completed in {} seconds. {} seconds per run.".format(num_runs, end_time, end_time/num_runs))
