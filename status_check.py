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

print("Number completed: {}, number remaining: {}, percentage complete: {}".format(num_completed, num_remaining, 100*(num_completed / (num_completed + num_remaining))))
