import glob
import pickle
import random

import numpy as np

from multiprocessing import Pool
from pathlib import Path

from util import is_carm, primesfrom2to


class Carm3:
    def __init__(self, upper_bound=1000, num_cores=1, data_folder='data'):
        self.upper_bound = upper_bound
        self.num_cores = num_cores
        self.data_folder = data_folder
        self.primes_to_check = primesfrom2to(self.upper_bound)
        self.p1_primes_to_check = self.primes_to_check

    def calculate(self):
        # Load primes_to_check from pickle file
        file_list = glob.glob(str(Path(self.data_folder + '/' + 'checked_carm_*')))
        if file_list:
            max_file_num = max([int(item.replace(str(Path(self.data_folder + '/' + 'checked_carm_')), '').replace('.pkl', '')) for item in file_list])
            p1_set = set()
            p1_list = []
            for n in range(1, max_file_num + 1):
                try:
                    filename = Path(self.data_folder + '/' + 'checked_carm_{}.pkl'.format(n))
                    infile = open(filename, 'rb')
                    existing_results = pickle.load(infile)
                    p1_list = p1_list + existing_results
                    infile.close()
                except Exception as e:
                    print(e)
            p1_set = set(p1_list)
            self.p1_primes_to_check = [p for p in self.primes_to_check if p not in p1_set]
        else:
            pass

        # Split primes into num_cores even segments
        random.shuffle(self.primes_to_check)
        n = self.num_cores - 1
        n_list_size = int(len(self.primes_to_check) / self.num_cores)
        split_primes = np.array_split(self.primes_to_check, self.num_cores)

        p = Pool(processes=self.num_cores)
        p.starmap(self._generate_3carm, [[i, split_primes[i]] for i in range(0, self.num_cores)])

    def _generate_3carm(self, core_num, p1_primes):
        p1_primes_to_check = [p for p in p1_primes if p in self.p1_primes_to_check]
        for p1 in p1_primes_to_check:
            p2_primes_to_check = [p for p in self.primes_to_check if p > p1]
            for p2 in p2_primes_to_check:
                p3_primes_to_check = [p for p in p2_primes_to_check if p > p2]
                for p3 in p3_primes_to_check:
                    candidate = p1 * p2 * p3
                    if is_carm(int(candidate)):
                        existing_results = []
                        new_result = [(p1, p2, p3, candidate)]
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
            filename = Path(self.data_folder + '/' + 'checked_carm_{}.pkl'.format(core_num))
            try:
                infile = open(filename, 'rb')
                existing_results = pickle.load(infile)
                infile.close()
                result = existing_results + [p1]
            except Exception as e:
                print(e)
                result = [p1]
            outfile = open(filename, 'wb')
            pickle.dump(result, outfile)
            outfile.close()

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
