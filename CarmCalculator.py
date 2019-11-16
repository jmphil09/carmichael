import glob
import pickle
import random
import numpy as np

from multiprocessing import Pool
from pathlib import Path

from util import primesfrom2to


INITIAL_PRIME_LIMIT = 10000


class CarmCalculator:
    def __init__(self, upper_bound=350, num_cores=1, data_folder='data'):
        self.upper_bound = upper_bound
        self.num_cores = num_cores
        self.data_folder = data_folder
        self.primes = primesfrom2to(upper_bound)
        self.p1_primes_to_check = self.primes
        self.large_primes = primesfrom2to(INITIAL_PRIME_LIMIT)

        file_list = glob.glob(str(Path(self.data_folder + '/' + 'checked_carm_*')))
        if file_list:
            max_file_num = max([int(item.replace(str(Path(self.data_folder + '/' + 'checked_carm_')), '').replace('.pkl', '')) for item in file_list])
            p1_set = set()
            p1_list = []
            for n in range(0, max_file_num + 1):
                try:
                    filename = Path(self.data_folder + '/' + 'checked_carm_{}.pkl'.format(n))
                    infile = open(filename, 'rb')
                    existing_results = pickle.load(infile)
                    p1_list = p1_list + existing_results
                    infile.close()
                except Exception as e:
                    print(e)
            p1_set = set(p1_list)
            self.p1_primes_to_check = [p for p in self.primes if p not in p1_set]
        else:
            pass

    def _is_prime(self, n):
        largest_prime = self.large_primes[-1]
        if n > largest_prime:
            increase_size = largest_prime * 2
            #print('_is_prime size has been increased to {}'.format(increase_size))
            self.large_primes = primesfrom2to(increase_size)
            return self._is_prime(n)
        else:
            return n in self.large_primes

    def calc_3_carms_for_p(self, current_prime, next_prime, core_num):
        try:
            m = current_prime
            diff = next_prime - current_prime
            k = diff

            for B in range(2, m):
                self.large_primes = primesfrom2to(INITIAL_PRIME_LIMIT)
                a = int(np.floor((np.power(m, 2) / B)) + 1)
                b = int(np.floor((1 / B) * (np.power(m, 2) + ((m + B) * (m - 1)) / (m + k - 1))))

                for A in range(a, b + 1):
                    p = 1 + ((m + B) * (m - 1)) / (A * B - np.power(m, 2))
                    q = (A * (p-1) + 1) / m
                    if np.floor(p) == p and np.floor(q) == q:  # np.floor(q) == q may not be needed
                        if self._is_prime(p) and self._is_prime(q):
                            x = (p * q - 1) / (m - 1)
                            y = (m * q - 1) / (p - 1)
                            z = (m * p - 1) / (q - 1)
                            if np.floor(x) == x and np.floor(y) == y and np.floor(z) == z:
                                p1 = np.longlong(m)
                                p2 = np.longlong(p)
                                p3 = np.longlong(q)
                                carm_num = np.uint64(p1*p2*p3)
                                #print((p1, p2, p3, carm_num))
                                existing_results = []
                                new_result = [(p1, p2, p3, carm_num)]
                                filename = Path(self.data_folder + '/' + 'found_carm_{}.pkl'.format(core_num))
                                try:
                                    save_dir = filename.parent
                                    save_dir.mkdir(parents=True, exist_ok=True)
                                    infile = open(filename, 'rb')
                                    existing_results = pickle.load(infile)
                                    infile.close()
                                    result = existing_results + new_result
                                except Exception as e:
                                    print(e)
                                    result = new_result
                                outfile = open(filename, 'wb')
                                pickle.dump(result, outfile)
                                outfile.close()
        except Exception as ex:
            print(ex)
            time.sleep(60)
            self.calc_3_carms_for_p(current_prime, next_prime, core_num)

    def calc_3_carms_for_list(self, prime_list, core_num):
        for i in range(0, len(prime_list)):
            current_prime = prime_list[i]
            next_prime = [p for p in self.sorted_primes if p > current_prime][0]
            self.calc_3_carms_for_p(current_prime, next_prime, core_num)

            filename = Path(self.data_folder + '/' + 'checked_carm_{}.pkl'.format(core_num))
            try:
                infile = open(filename, 'rb')
                existing_results = pickle.load(infile)
                infile.close()
                result = existing_results + [current_prime]
            except Exception as e:
                print(e)
                result = [current_prime]
            save_dir = filename.parent
            save_dir.mkdir(parents=True, exist_ok=True)
            outfile = open(filename, 'wb')
            pickle.dump(result, outfile)
            outfile.close()

    def calc_3_carms(self):
        new_limit = self.upper_bound
        while not self._is_prime(new_limit):
            new_limit += 1
        random.shuffle(self.p1_primes_to_check)  # This may cause performance increases with higher core counts
        split_primes = np.array_split(self.p1_primes_to_check, self.num_cores)
        self.sorted_primes = sorted(primesfrom2to(new_limit + 1))

        p = Pool(processes=self.num_cores)
        p.starmap(self.calc_3_carms_for_list, [[split_primes[i], i] for i in range(0, self.num_cores)])

    def _display_results(self):
        carm_list = []
        file_list = glob.glob(str(Path(self.data_folder + '/' + 'found_carm_*')))
        if file_list:
            max_file_num = max([int(item.replace(str(Path(self.data_folder + '/' + 'found_carm_')), '').replace('.pkl', '')) for item in file_list])
            for n in range(0, max_file_num + 1):
                try:
                    filename = Path(self.data_folder + '/' + 'found_carm_{}.pkl'.format(n))
                    infile = open(filename, 'rb')
                    existing_results = pickle.load(infile)
                    carm_list = carm_list + existing_results
                    infile.close()
                except Exception as e:
                    print(e)
        carm_list = sorted(list(set(carm_list)))
        print(sorted(carm_list))
        print(len(carm_list))
