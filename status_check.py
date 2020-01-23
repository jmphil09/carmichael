from db_commands import retrieve_items


USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'


completed = retrieve_items(100000, table='selected_items', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')
num_completed = len(completed)
remaining = retrieve_items(100000, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')
num_remaining = len(remaining)

print("Number completed: {}, number remaining: {}, percentage complete: {}".format(num_completed, num_remaining, 100*(num_completed / num_remaining)))
