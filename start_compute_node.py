import json
import os
import requests
import time
from shutil import rmtree

import compute_node_config
from CarmNodeCalculator import CarmNodeCalculator


if __name__ == '__main__':
    calculator = CarmNodeCalculator(
        workload_url=compute_node_config.WORKLOAD_URL,
        result_url=compute_node_config.RESULT_URL,
        num_cores=compute_node_config.NUM_CORES,
        batch_size=compute_node_config.BATCH_SIZE,
        wait_time=compute_node_config.WAIT_TIME,
        batch_increase_time=compute_node_config.BATCH_INCREASE_TIME,
        batch_decrease_time=compute_node_config.BATCH_DECREASE_TIME
    )
    calculator.main()
