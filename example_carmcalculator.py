from CarmCalculator import CarmCalculator

import time
start_time = time.perf_counter()


if __name__ == '__main__':
    c3 = CarmCalculator(
        upper_bound=1000,
        num_cores=32,
        data_folder='3carm_example'
    )
    #c3.calc_3_carms_for_p(347, 349, 0)
    c3.calc_3_carms()
    end_time = time.perf_counter()
    print("Completed in {} seconds.".format(int(end_time - start_time)))

#upper_boud=700, no prime scrambling
#Completed in 42 seconds.- 1 core
#Completed in 40 seconds.- 2 cores
#Completed in 30 seconds.- 4 cores
#Completed in 18 seconds.- 8 cores
#Completed in 14 seconds.- 12 cores
#Completed in 12 seconds.- 16 cores
#Completed in 11 seconds.- 20 cores
#Completed in 9 seconds.- 24 cores
#Completed in 7 seconds. - 32 cores

#upper_boud=700, prime scrambling
#Completed in 47 seconds.- 1 core
#Completed in 26 seconds.- 2 cores
#Completed in 16 seconds.- 4 cores
#Completed in 11 seconds.- 8 cores
#Completed in 11 seconds.- 12 cores
#Completed in 7 seconds.- 16 cores
#Completed in 10 seconds.- 20 cores
#Completed in 11 seconds.- 24 cores
#Completed in 10 seconds. - 32 cores


#upper_boud=1000, no prime scrambling
#Completed in 159 seconds.- 1 core
#Completed in 149 seconds.- 2 cores
#Completed in 112 seconds.- 4 cores
#Completed in 71 seconds.- 8 cores
#Completed in 49 seconds.- 12 cores
#Completed in 43 seconds.- 16 cores
#Completed in 33 seconds.- 20 cores
#Completed in 34 seconds.- 24 cores
#Completed in 31 seconds. - 32 cores

#upper_boud=1000, prime scrambling
#Completed in 162 seconds.- 1 core
#Completed in 94 seconds.- 2 cores
#Completed in 60 seconds.- 4 cores
#Completed in 38 seconds.- 8 cores
#Completed in 36 seconds.- 12 cores
#Completed in 34 seconds.- 16 cores
#Completed in 31 seconds.- 20 cores
#Completed in 33 seconds.- 24 cores
#Completed in 32 seconds. - 32 cores


#Make fancy graph of #cores vs #seconds
#Write a hashmap is_prime function
#Pickle the results
#Create checkpoints
