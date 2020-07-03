import db_commands
import db_config

from util import primesfrom2to


USER = db_config.USER
PASSWORD = db_config.PASSWORD
HOST = db_config.HOST
PORT = db_config.PORT
DATABASE = db_config.DATABASE
DATABASE_RESULTS = db_config.DATABASE_RESULTS


results = db_commands.retrieve_items(1000000, table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')

p1s = sorted(list(set([factors[0] for factors in results])))
p2s = sorted(list(set([factors[1] for factors in results])))
p3s = sorted(list(set([factors[2] for factors in results])))
possible_p1s = primesfrom2to(p1s[-1] + 1)
exceptional_primes = [p for p in possible_p1s if p not in p1s]
exceptional_primes = [p for p in exceptional_primes if p > 2]


print('=======================================================')
print('Number of 3-Carmichael numbers with p1 < 1,000,000: {}'.format(len(results)))
print('Number of exception primes with p1 < 1,000,000: {}'.format(len(exceptional_primes)))
print('=======================================================')

print('=======================================================')
print('Exceptional Primes')
print(exceptional_primes)
print('=======================================================')
