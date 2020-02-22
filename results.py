import db_commands
import db_config


USER = db_config.USER
PASSWORD = db_config.PASSWORD
HOST = db_config.HOST
PORT = db_config.PORT
DATABASE = db_config.DATABASE
DATABASE_RESULTS = db_config.DATABASE_RESULTS


#db_commands.get_results()
results = db_commands.retrieve_items(1000000, table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')

print('Number of 3-Carmichael numbers with p1 < 1,000,000: {}'.format(len(results)))
