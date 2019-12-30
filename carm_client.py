import json
import requests
from shutil import rmtree

from CarmCalculator import CarmCalculator


# TODO: Put these values in a config file
WORKLOAD_URL = 'http://192.168.50.160:9000/get_workload'
RESULT_URL = 'http://192.168.50.160:9000/send_results'
NUM_CORES = 1
BATCH_SIZE = 1



def main(algorithm_to_use, range_start, range_stop, batch, num_cores):
    if algorithm_to_use=='carm3':  # TODO: Add support for other algorithms
        c3 = CarmCalculator(
            lower_bound=range_start,
            upper_bound=range_stop,
            batch=batch,
            num_cores=num_cores
        )
        result = c3.calc_3_carms()
        return result
    else:
        print('Unknown Algorithm')


if __name__ == '__main__':
    finished = False
    while not finished:
        PARAMS = {
            'num_cores': NUM_CORES,
            'batch_size': BATCH_SIZE
        }
        import time
        start_time = time.perf_counter()
        workload_response = requests.get(url=WORKLOAD_URL, params=PARAMS).json()
        print(workload_response)
        algorithm_to_use = workload_response['algorithm_to_use']
        numbers_to_compute = workload_response['numbers_to_compute']
        finished = workload_response['finished']
        if finished:
            break
        range_start = min(numbers_to_compute)
        range_stop = max(numbers_to_compute)

        result = main(algorithm_to_use, range_start, range_stop, numbers_to_compute, NUM_CORES)

        #POST the result to the server
        json_result = {
            'result': result
        }
        requests.post(RESULT_URL, json=json_result)

        end_time = time.perf_counter()
        run_time = int(end_time - start_time)
        print("Completed in {} seconds.".format(run_time))
        if run_time < 60: # If run_time < 1 min: increase the batch_size
            BATCH_SIZE = 2 * BATCH_SIZE
            print('Increasing batch size to {}'.format(BATCH_SIZE))
        elif run_time > 600: # If run_time > 10 mins: decrease batch_size
            BATCH_SIZE = int(BATCH_SIZE / 2)
            print('Decreasing batch size to {}'.format(BATCH_SIZE))
        else:
            print('Keeping batch size at {}'.format(BATCH_SIZE))
