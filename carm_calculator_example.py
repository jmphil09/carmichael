import time

from CarmCalculator import CarmCalculator


'''
Before continuing, make sure you set up and activate a virtual environment
according to the README.

Run this script with `python3 carm_calculator_example.py`. While running, you
will see a progress bar for each cpu core used.

The output of this script will be a list of Carmichael numbers of the form
(p1, p2, p3) where p1 < p2 < p3, followed by the number of seconds the script
took to run.
'''

# Tunable parameters
# Play around with these values to get a feel for how the CarmCalculator class works
LOWER_BOUND = 3  # The lowest p1 prime number to use to create 3-Carmichael numbers of the form: p1*p2*p3 where p1 < p2 < p3
UPPER_BOUND = 1000  # The highest p1 prime number to use to create 3-Carmichael numbers of the form: p1*p2*p3 where where p1 < p2 < p3
NUM_CORES = 1  # The number of cpu cores to use. Compare using 1 with the number of cpu cores your system has to see vast improvements.

start_time = time.time()
calculator = CarmCalculator(
    lower_bound=LOWER_BOUND,
    upper_bound=UPPER_BOUND,
    num_cores=NUM_CORES
)

result = calculator.calc_3_carms()
end_time = time.time()
print(result)
print('Runtime: {} seconds'.format(int(end_time-start_time)))
