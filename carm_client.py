import json
import requests
from shutil import rmtree

from CarmCalculator import CarmCalculator


# TODO: Put these values in a config file
WORKLOAD_URL = 'http://192.168.50.160:9000/get_workload'
RESULT_URL = 'http://192.168.50.160:9000/send_results'
NUM_CORES = 16
BATCH_SIZE = 99
PARAMS = {
    'num_cores': NUM_CORES,
    'batch_size': BATCH_SIZE
}


def main(algorithm_to_use, range_start, range_stop, num_cores):
    if algorithm_to_use=='carm3':  # TODO: Add support for other algorithms
        c3 = CarmCalculator(
            lower_bound=range_start,
            upper_bound=range_stop,
            num_cores=num_cores
        )
        result = c3.calc_3_carms()
        return result
    else:
        print('Unknown Algorithm')


if __name__ == '__main__':
    finished = False
    while not finished:
        import time
        start_time = time.perf_counter()
        workload_response = requests.get(url=WORKLOAD_URL, params=PARAMS).json()
        print(workload_response)
        algorithm_to_use = workload_response['algorithm_to_use']
        numbers_to_compute = workload_response['numbers_to_compute']
        finished = workload_response['finished']
        range_start = numbers_to_compute[0]
        range_stop = numbers_to_compute[1]

        result = main(algorithm_to_use, range_start, range_stop, NUM_CORES)

        #POST the result to the server
        json_result = {
            'result': result
        }
        requests.post(RESULT_URL, json=json_result)
        end_time = time.perf_counter()
        run_time = int(end_time - start_time)
        # TODO: If run_time > 10 mins (or some other value), decrease batch_size
        # If run_time < 1 min, increase the batch_size
        print("Completed in {} seconds.".format(run_time))
