from Carm3 import Carm3

import time
start_time = time.perf_counter()


if __name__ == '__main__':
    c3 = Carm3(upper_bound=1000, num_cores=16, data_folder='carm_1000')
    c3.calculate()
    end_time = time.perf_counter()
    print("Completed in {} seconds.".format(end_time - start_time))
    c3._display_results()
