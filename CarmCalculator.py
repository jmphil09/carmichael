import glob
import pickle
import random
import time
import numpy as np

from multiprocessing import Pool
from pathlib import Path

from util import primesfrom2to


INITIAL_PRIME_LIMIT = 10000


class CarmCalculator:
    def __init__(self, upper_bound=350, num_cores=1, data_folder='data', percentage_marker=5):
        self.upper_bound = upper_bound
        self.num_cores = num_cores
        self.data_folder = data_folder
        self.primes = primesfrom2to(self.upper_bound)
        self.p1_primes_to_check = self.primes
        self.percentage_marker = percentage_marker
        self.primes_per_core = {k:0 for k in range(0, num_cores)}
        self.prime_dict = {}

        file_list = glob.glob(str(Path(self.data_folder + '/' + 'checked_carm_*')))
        if file_list:
            max_file_num = max([int(item.replace(str(Path(self.data_folder + '/' + 'checked_carm_')), '').replace('.pkl', '')) for item in file_list])
            p1_set = set()
            p1_list = []
            for n in range(0, max_file_num + 1):
                try:
                    filename = Path(self.data_folder + '/' + 'checked_carm_{}.pkl'.format(n))
                    with open(filename, 'rb') as infile:
                        existing_results = pickle.load(infile)
                        self.primes_per_core[n] = len(existing_results)
                        p1_list = p1_list + existing_results
                except Exception as e:
                    print('Exception occured in initializing class')
                    print(e)
                    pass
            p1_set = set(p1_list)
            self.p1_primes_to_check = [p for p in self.primes if p not in p1_set]
            assert len(self.p1_primes_to_check) == len(self.primes) - sum(self.primes_per_core.values())


    def _is_prime(self, n):
        if n == 2 or n == 3:
            return True
        elif n < 2 or n % 2 == 0:
            return False
        elif n < 9:
            return True
        elif n % 3 == 0:
            return False
        r = int(np.sqrt(n))
        f = 5
        while f <= r:
            if n % f == 0 or n % (f + 2) == 0:
                return False
            else:
                f += 6
        return True

    def is_prime(self, n):
        result = self.prime_dict.get(n, None)
        if not result:
            self.prime_dict[n] = self._is_prime(n)
        return self.prime_dict[n]


    def next_prime(self, n):
        # Base case
        if (n <= 1):
            return 2

        prime = n
        found = False

        # Loop continuously until isPrime returns
        # True for a number greater than n
        while(not found):
            prime = prime + 1

            if(self.is_prime(prime) == True):
                found = True

        return prime




    def calc_3_carms_for_p(self, current_prime, next_prime, core_num):
        try:
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
                        if self.is_prime(p) and self.is_prime(q):
                            x = (p * q - 1) / (m - 1)
                            y = (m * q - 1) / (p - 1)
                            z = (m * p - 1) / (q - 1)
                            if np.floor(x) == x and np.floor(y) == y and np.floor(z) == z:
                                existing_results = []
                                new_result = [(m, int(p), int(q))]  # [(p1, p2, p3)]
                                try:
                                    filename = Path(self.data_folder + '/' + 'found_carm_{}.pkl'.format(core_num))
                                    try:
                                        save_dir = filename.parent
                                        save_dir.mkdir(parents=True, exist_ok=True)
                                        with open(filename, 'rb', 0) as infile:
                                        #with open(filename, 'rb') as infile:
                                            existing_results = pickle.load(infile)
                                        result = existing_results + new_result
                                    except Exception as e:
                                        print('Exception occured in calc_3_carms_for_p 0')
                                        print(e)
                                        result = new_result
                                    with open(filename, 'wb', 0) as outfile:
                                        pickle.dump(result, outfile)
                                except Exception as e:
                                    print('Exception occured in calc_3_carms_for_p 1')
                                    print(e)

            filename = Path(self.data_folder + '/' + 'checked_carm_{}.pkl'.format(core_num))
            try:
                with open(filename, 'rb', 0) as infile:
                    existing_results = pickle.load(infile)
                result = existing_results + [current_prime]
            except Exception as e:
                print('Exception occured in calc_3_carms_for_p 2')
                print(e)
                result = [current_prime]

            save_dir = filename.parent
            save_dir.mkdir(parents=True, exist_ok=True)
            with open(filename, 'wb', 0) as outfile:
                pickle.dump(result, outfile)

        except Exception as ex:
            print('Exception occured in calc_3_carms_for_p 3')
            print(ex)
            time.sleep(60)
            self.calc_3_carms_for_p(current_prime, next_prime, core_num)

    def calc_3_carms_for_list(self, prime_list, core_num):
        total_primes = len(self.primes) + 1
        print_marker = int(total_primes / (100 / self.percentage_marker))
        prime_counter = self.primes_per_core[core_num]
        for i in range(0, len(prime_list)):
            if prime_counter % print_marker == 0:
                percent = int((prime_counter / (total_primes))*100)
                complete_bar = '|' + '='*percent + '-'*(100-percent) + '|'
                print('Core {}: {}% {}'.format(core_num, percent, complete_bar))
            prime_counter += 1
            current_prime = prime_list[i]
            next_prime = self.next_prime(current_prime)
            self.calc_3_carms_for_p(current_prime, next_prime, core_num)


    def calc_3_carms(self):
        if len(self.p1_primes_to_check) > 0:
            new_limit = self.upper_bound
            while not self.is_prime(new_limit):
                new_limit += 1
            random.shuffle(self.p1_primes_to_check)  # This may cause performance increases with higher core counts
            split_primes = np.array_split(self.p1_primes_to_check, self.num_cores)
            p = Pool(processes=self.num_cores)
            p.starmap(self.calc_3_carms_for_list, [[split_primes[i], i] for i in range(0, self.num_cores)])

    def _display_results(self):
        carm_list = []
        file_list = glob.glob(str(Path(self.data_folder + '/' + 'found_carm_*')))
        if file_list:
            max_file_num = max([int(item.replace(str(Path(self.data_folder + '/' + 'found_carm_')), '').replace('.pkl', '')) for item in file_list])
            for n in range(0, max_file_num + 1):
                print('===')
                print(n)
                try:
                    filename = Path(self.data_folder + '/' + 'found_carm_{}.pkl'.format(n))
                    with open(filename, 'rb') as infile:
                        existing_results = pickle.load(infile)
                        carm_list = carm_list + existing_results
                except Exception as e:
                    print('Exception occured in _display_results')
                    print(e)
        #print(sorted(carm_list, key=lambda x: x[1])[0:100])

        carm_list = sorted(list(set(carm_list)))
        #print(len(carm_list))
        return carm_list

    def _display_found_p1(self):
        carm_list = self._display_results()
        p1_list = sorted(list(set([p[0] for p in carm_list])))
        p2_list = sorted(list(set([p[1] for p in carm_list])))
        p3_list = sorted(list(set([p[2] for p in carm_list])))
        #print(p1_list)
        print('Number of p1\'s found: {}'.format(len(p1_list)))
        all_primes = primesfrom2to(self.upper_bound)
        print('All primes below {}: {}'.format(self.upper_bound, len(all_primes)))
        print('Number of exceptional_primes: {}'.format(len(all_primes) - len(p1_list)))
        exceptional_primes = [p for p in all_primes if p not in p1_list]
        exceptional_primes = exceptional_primes[1::]
        print('Number of exceptional primes: {}'.format(len(exceptional_primes)))
        print('First 10 p1\'s: {}'.format(p1_list[0:10]))
        print('First 10 exceptional primes: {}'.format(exceptional_primes[0:10]))
        #print(carm_list[0:100])
