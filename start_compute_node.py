import json
import os
import requests
import time
from shutil import rmtree

import compute_node_config
from CarmCalculator import CarmCalculator


# Constants
WORKLOAD_URL = compute_node_config.WORKLOAD_URL
RESULT_URL = compute_node_config.RESULT_URL
NUM_CORES = compute_node_config.NUM_CORES
BATCH_SIZE = compute_node_config.BATCH_SIZE
WAIT_TIME = compute_node_config.WAIT_TIME
BATCH_INCREASE_TIME = compute_node_config.BATCH_INCREASE_TIME
BATCH_DECREASE_TIME = compute_node_config.BATCH_DECREASE_TIME


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


def increase_batch(current_batch):
    result = 2 * current_batch
    while result % NUM_CORES != 0:
        result += 1
    return result


def decrease_batch(current_batch):
    result = int(current_batch / 2)
    while result % NUM_CORES != 0:
        result += 1
    return result


if __name__ == '__main__':
    finished = False
    while True:
        try:
            PARAMS = {
                'num_cores': NUM_CORES,
                'batch_size': BATCH_SIZE
            }
            start_time = time.perf_counter()
            workload_response = requests.get(url=WORKLOAD_URL, params=PARAMS).json()
            print(workload_response)
            algorithm_to_use = workload_response['algorithm_to_use']
            numbers_to_compute = workload_response['numbers_to_compute']
            finished = workload_response['finished']

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
            if run_time < BATCH_INCREASE_TIME: # If run_time < 1 min: increase the batch_size
                BATCH_SIZE = increase_batch(BATCH_SIZE)
                print('Increasing batch size to {}'.format(BATCH_SIZE))
            elif run_time > BATCH_DECREASE_TIME: # If run_time > 10 mins: decrease batch_size
                BATCH_SIZE = decrease_batch(BATCH_SIZE)
                print('Decreasing batch size to {}'.format(BATCH_SIZE))
            else:
                print('Keeping batch size at {}'.format(BATCH_SIZE))
        except Exception as ex:
            print(ex)
            time.sleep(WAIT_TIME)