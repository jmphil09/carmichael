import psycopg2
from psycopg2 import Error


#TODO: Put these values in a config file
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'

#TODO: Add docstrings


def create_table(table, user, password, host, port, database):
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()

        create_table_query = '''
            CREATE TABLE {}
                (
                ID INT PRIMARY KEY NOT NULL,
                NUM INT NOT NULL,
                ALGORITHM TEXT NOT NULL
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

        insert_query = '''INSERT INTO {} (ID, NUM, ALGORITHM) VALUES (%s,%s,%s)'''.format(table)

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

        delete_query = '''Delete from {} where id = %s'''.format(table)

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


#create_table(table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')
#records = [(8, 8, 'carm3'), (9, 9, 'carm3')]
#records = [(n, n, 'carm3') for n in range(3, 100)]
#insert_items(records, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')
#delete_items(records, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute')
#print(retrieve_items(100, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database='numbers_to_compute'))
