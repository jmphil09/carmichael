import requests
from shutil import rmtree

from CarmCalculator import CarmCalculator


#URL = 'http://127.0.0.1:5000/'
URL = 'http://192.168.50.160:9000/'
NUM_CORES = 16
PARAMS = {
    'num_cores': NUM_CORES
}
DATA_DIR = 'temp_compute'


response = requests.get(url=URL, params=PARAMS)
response = response.json()
algorithm_to_use = response['algorithm_to_use']
numbers_to_compute = response['numbers_to_compute']
range_start = numbers_to_compute[0]
range_stop = numbers_to_compute[1]
range_step = numbers_to_compute[2]
compute_range = range(range_start, range_stop, range_step)

print(response)
'''print(algorithm_to_use)
print(numbers_to_compute)
print(range_start)
print(range_stop)
print(range_step)
print(compute_range)'''

#clear the data folder
def clear_data_dir(dir='data'):
    try:
        rmtree(dir)
    except Exception as ex:
        print("{} directory does not exist".format(dir))
        print(ex)

def main():
    clear_data_dir(DATA_DIR)
    if algorithm_to_use=='carm3':
        c3 = CarmCalculator(
            upper_bound=range_stop,
            num_cores=NUM_CORES,
            data_folder=DATA_DIR
        )
        c3.calc_3_carms()
        c3._display_results()
        c3._display_found_p1()
    else:
        print('Unknown Algorithm')


if __name__ == '__main__':
    main()
