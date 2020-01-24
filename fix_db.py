from db_commands import delete_items, insert_items, retrieve_items


DATABASE = 'numbers_to_compute'
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'


not_finished = [(p[0], p[1]) for p in retrieve_items(10000000, table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')]
insert_items(not_finished, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
delete_items(not_finished, table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
