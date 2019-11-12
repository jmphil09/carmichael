import time

from util import is_carm


start_time = time.perf_counter()


LIMIT = 10000


def standard(limit):
    carm_list = []
    for num in range(limit + 1):
        if is_carm(num):
            carm_list.append(num)
    return carm_list


def better(limit):
    carm_list = [n for n in range(limit + 1) if is_carm(n)]
    return carm_list


# standard(LIMIT)  # Run time: 6.7382412
# better(LIMIT)  # Run time: 6.7175443

end_time = time.perf_counter()
run_time = end_time - start_time
print('Run time: {}'.format(run_time))
