import psycopg2
from psycopg2 import Error

import db_config
from util import primesfrom2to


#Allow psycopg2 to use numpy 64 bit numbers
import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)


USER = db_config.USER
PASSWORD = db_config.PASSWORD
HOST = db_config.HOST
PORT = db_config.PORT
DATABASE = db_config.DATABASE
DATABASE_RESULTS = db_config.DATABASE_RESULTS

#TODO: Add docstrings


def create_table(table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        create_table_query = '''
            CREATE TABLE if not exists {}
                (
                NUM INT NOT NULL UNIQUE,
                ALG TEXT NOT NULL
                ); '''.format(table)

        cursor.execute(create_table_query)
        connection.commit()
        print('Table {} created successfully in database {}'.format(table, database))

    except Exception as ex:
        print('An error occured in create_table.')
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection closed')


def create_table_results(table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        create_table_query = '''
            CREATE TABLE if not exists {}
                (
                p1 BIGINT NOT NULL,
                p2 BIGINT NOT NULL,
                p3 BIGINT NOT NULL,
                alg TEXT NOT NULL,
                ipaddr TEXT NOT NULL,
                ts TEXT NOT NULL
                ); '''.format(table)

        cursor.execute(create_table_query)
        connection.commit()
        print('Table {} created successfully in database {}'.format(table, database))

    except Exception as ex:
        print('An error occured in create_table.')
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection closed')



def insert_items(records, table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        insert_query = '''INSERT INTO {} (NUM, ALG) VALUES (%s,%s) ON CONFLICT (NUM) DO NOTHING;'''.format(table, table)

        cursor.executemany(insert_query, records)
        connection.commit()

        count = cursor.rowcount
        print('{} Records inserted into {}'.format(count, table))

    except Exception as ex:
        print('An error occured in insert_items.')
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection closed')



def insert_results(records, table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        insert_query = '''INSERT INTO {} (p1, p2, p3, alg, ipaddr, ts) VALUES (%s,%s,%s,%s,%s,%s);'''.format(table)

        cursor.executemany(insert_query, records)
        connection.commit()

        count = cursor.rowcount
        print('{} Records inserted into {}'.format(count, table))

    except Exception as ex:
        print('An error occured in insert_items.')
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection closed')



def delete_items(records, table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        delete_query = '''Delete from {} where NUM = %s'''.format(table)

        ids = [[record[0]] for record in records]
        cursor.executemany(delete_query, ids)
        connection.commit()

        count = cursor.rowcount
        print('{} Records deleted from {}'.format(count, table))

    except Exception as ex:
        print('An error occured in delete_items.')
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection closed')


def retrieve_items(num_items, table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        retrieve_query = '''SELECT * FROM {} ORDER BY RANDOM() LIMIT {}'''.format(table, num_items)

        cursor.execute(retrieve_query)
        connection.commit()

        count = cursor.rowcount
        print('{} Records retrieved from {}'.format(count, table))

        return cursor.fetchall()

    except Exception as ex:
        print('An error occured in retrieve_items.')
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection closed')


def create_all_tables():
    create_table(table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    create_table(table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    create_table(table='selected_items', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    create_table_results(table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

def populate_queue():
    records = [(n, 'carm3') for n in primesfrom2to(10000)[1:]]
    #records = [(n, m) for n in primesfrom2to(1000)[1:] for m in ['carm3', 'carm4']]
    insert_items(records, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

def get_results():
    items = retrieve_items(10000, table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    print(items)

def delete_tables():
    table_names = ['results', 'computing_table', 'numbers_to_compute', 'selected_items']
    for table in table_names:
        connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        cursor = connection.cursor()
        delete_query = '''DROP TABLE if exists {}'''.format(table)
        cursor.execute(delete_query)
        connection.commit()
        cursor.close()
        connection.close()
