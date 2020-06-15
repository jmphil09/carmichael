import time
#start = time.time()
from CarmCalculator import CarmCalculator

#calculator = CarmCalculator(lower_bound = 3, upper_bound=10000, batch=None, num_cores=16, data_folder='tr_data')
#calculator.calc_3_carms()

#end = time.time()
#print('Runtime: {} seconds'.format(int(end-start)))


def time_test(core_list):
    result = []
    for num_cores in core_list:
        start_time = time.time()
        calculator = CarmCalculator(lower_bound = 3, upper_bound=10000, batch=None, num_cores=num_cores, data_folder='tr_data')
        calculator.calc_3_carms()
        end_time = time.time()
        result.append('Runtime for {} cores: {} seconds'.format(num_cores, int(end_time-start_time)))
    return result


cores_to_test = [1, 2, 4, 8, 16, 24, 32, 48, 64, 96, 128]
result = time_test(cores_to_test)
print(result)
'''
1950x
['Runtime for 1 cores: 584 seconds'
 'Runtime for 2 cores: 299 seconds'
 'Runtime for 4 cores: 152 seconds'
 'Runtime for 8 cores: 80 seconds'
 'Runtime for 16 cores: 39 seconds'
 'Runtime for 24 cores: 35 seconds'
 'Runtime for 32 cores: 31 seconds']

 ['Runtime for 48 cores: 29 seconds',
  'Runtime for 64 cores: 29 seconds']

2990wx
['Runtime for 1 cores: 540 seconds',
 'Runtime for 2 cores: 275 seconds',
 'Runtime for 4 cores: 138 seconds',
 'Runtime for 8 cores: 74 seconds',
 'Runtime for 16 cores: 42 seconds',
 'Runtime for 24 cores: 29 seconds',
 'Runtime for 32 cores: 25 seconds',
 'Runtime for 48 cores: 21 seconds',
 'Runtime for 64 cores: 20 seconds',
 'Runtime for 96 cores: 19 seconds',
 'Runtime for 128 cores: 18 seconds']
'''
