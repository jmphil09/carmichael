from datetime import datetime

import db_config

from db_commands import retrieve_items


USER = db_config.USER
PASSWORD = db_config.PASSWORD
HOST = db_config.HOST
PORT = db_config.PORT
DATABASE = db_config.DATABASE
DATABASE_RESULTS = db_config.DATABASE_RESULTS


completed = retrieve_items(100000, table='selected_items', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
num_completed = len(completed)
remaining = retrieve_items(100000, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
num_remaining = len(remaining)

print('=======================================================')
print("Number completed: {}, number remaining: {}, percentage complete: {}".format(num_completed, num_remaining, 100*(num_completed / (num_completed + num_remaining))))
print('=======================================================')

all_items = retrieve_items(100000, table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
times = [datetime.fromisoformat(item[5]) for item in all_items]
beginning = min(times)
end = max(times)

print('=======================================================')
print('Runtime: {}'.format(end - beginning))
print('=======================================================')

print('=======================================================')
print('Results by ip address')
ip_addresses = [item[4].split(':')[0] for item in all_items]
ip_count = {ip_add : ip_addresses.count(ip_add) for ip_add in ip_addresses}
#print(ip_count)
for key,value in ip_count.items():
    print('{}: {}'.format(key, value))
print('=======================================================')
