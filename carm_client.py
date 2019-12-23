import requests
from shutil import rmtree

from CarmCalculator import CarmCalculator


URL = 'http://192.168.50.160:9000/'
NUM_CORES = 16
PARAMS = {
    'num_cores': NUM_CORES
}


response = requests.get(url=URL, params=PARAMS)
response = response.json()
algorithm_to_use = response['algorithm_to_use']
numbers_to_compute = response['numbers_to_compute']
range_start = numbers_to_compute[0]
range_stop = numbers_to_compute[1]
range_step = numbers_to_compute[2]

print(response)


def main():
    if algorithm_to_use=='carm3':
        c3 = CarmCalculator(
            lower_bound=range_start,
            upper_bound=range_stop,
            num_cores=NUM_CORES
        )
        result = c3.calc_3_carms()
        return result
    else:
        print('Unknown Algorithm')


if __name__ == '__main__':
    calculate_more = True
    while calculate_more:
        result = main()

        #POST the result to the server
        print(result)

        #The server will return True or False
        calculate_more = False
