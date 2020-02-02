import json
import numpy as np
import os
import requests
import time

from multiprocessing import Pool
from shutil import rmtree

import compute_node_config


class CarmNodeCalculator:
    def __init__(
        self,
        workload_url='http://192.168.50.160:9000/get_workload',
        result_url='http://192.168.50.160:9000/send_results',
        num_cores=4,
        batch_size=4,
        wait_time=300,
        batch_increase_time=120,
        batch_decrease_time=300
    ):
        self.workload_url = workload_url
        self.result_url = result_url
        self.num_cores = num_cores
        self.batch_size = batch_size
        self.wait_time = wait_time
        self.batch_increase_time = batch_increase_time
        self.batch_decrease_time = batch_decrease_time
        self.prime_dict = {}

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

            if(self.is_prime(prime)):
                found = True

        return prime

    def calc_3_carms_for_p(self, current_prime, next_prime, algorithm_to_use):
        try:
            result = []
            m = np.uint64(current_prime)
            diff = np.uint64(next_prime - current_prime)
            k = diff

            for B in np.arange(2, m):
                a = np.uint64(np.floor((np.power(m, 2) / B)) + 1)
                b = np.uint64(np.floor((1 / B) * (np.power(m, 2) + ((m + B) * (m - 1)) / (m + k - 1))))
                for A in np.arange(a, b + 1):
                    p = np.float64(1 + ((m + B) * (m - 1)) / (A * B - np.power(m, 2)))
                    q = np.float64((A * (p-1) + 1) / m)
                    if np.floor(p) == p and np.floor(q) == q:  # np.floor(q) == q may not be needed
                        if self.is_prime(p) and self.is_prime(q):
                            x = np.float64((p * q - 1) / (m - 1))
                            y = np.float64((m * q - 1) / (p - 1))
                            z = np.float64((m * p - 1) / (q - 1))
                            if np.floor(x) == x and np.floor(y) == y and np.floor(z) == z:
                                new_result = [(int(m), int(p), int(q), algorithm_to_use)]  # [(p1, p2, p3)]
                                result = result + new_result
            return result

        except Exception as ex:
            print('Exception occured in calc_3_carms_for_p 3')
            print(ex)
            time.sleep(60)
            self.calc_3_carms_for_p(current_prime, next_prime, algorithm_to_use)


    def compute(self, core_num):
        finished = False
        while True:
            try:
                PARAMS = {
                    'num_cores': self.num_cores,
                    'batch_size': self.batch_size
                }
                start_time = time.perf_counter()
                workload_response = requests.get(url=self.workload_url, params=PARAMS).json()
                print(workload_response)
                algorithm_to_use = workload_response['algorithm_to_use']
                numbers_to_compute = workload_response['numbers_to_compute']
                finished = workload_response['finished']

                result = []
                for num in numbers_to_compute:
                    next_num = self.next_prime(num)
                    result = result + self.calc_3_carms_for_p(num, next_num, algorithm_to_use)

                result = (result, [(n, algorithm_to_use) for n in numbers_to_compute])
                #POST the result to the server
                json_result = {
                    'result': result
                }

                requests.post(self.result_url, json=json_result)

                end_time = time.perf_counter()
                run_time = int(end_time - start_time)
                print("Completed in {} seconds.".format(run_time))
                # Try to satisfy self.batch_increase_time < actual time < self.batch_decrease_time
                if run_time < self.batch_increase_time:
                    self.batch_size += 1
                    print('Increasing batch size to {}'.format(self.batch_size))
                elif run_time > self.batch_decrease_time and self.batch_size > 1:
                    self.batch_size -= 1
                    print('Decreasing batch size to {}'.format(self.batch_size))
                else:
                    print('Keeping batch size at {}'.format(self.batch_size))
                if finished:
                    time.sleep(self.wait_time)
            except Exception as ex:
                print(ex)
                time.sleep(self.wait_time)

    def main(self):
        p = Pool(processes=self.num_cores)
        p.starmap(self.compute, [[i] for i in range(0, self.num_cores)])
