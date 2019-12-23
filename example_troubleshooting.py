from CarmCalculatorLegacy import CarmCalculator

import time
start_time = time.perf_counter()


if __name__ == '__main__':
    c3 = CarmCalculator(
        upper_bound=1000,
        num_cores=1,
        data_folder='troubleshooting'
    )
    c3.calc_3_carms()
    c3._display_results()
    c3._display_found_p1()
    end_time = time.perf_counter()
    print("Completed in {} seconds.".format(int(end_time - start_time)))
