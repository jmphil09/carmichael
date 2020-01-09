from flask import Flask, request

from db_commands import insert_items, delete_items, retrieve_items, insert_results


#GLOBAL_NUMS_TO_COMPUTE = list(range(3, 1000)) #TODO: replace with DB
#GLOBAL_RESULTS = [] #TODO: replace with DB

#TODO: Put these values in a config file
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'numbers_to_compute'
DATABASE_RESULTS = 'results'

#TODO: Add docstrings

app = Flask(__name__)


'''def get_json_response(batch_size):
    global GLOBAL_NUMS_TO_COMPUTE
    #TODO: Get 'batch_size' items from the worker queue DB
    # Add these values in memory to current_workload_list
    # if the values are in current_workload_list for > 60 mins, remove them
    #Idea: get batch_size items from DB that are NOT in current_workload_list
    algorithm_to_use = 'carm3'  # Also determined from worker queue DB
    numbers_to_compute = GLOBAL_NUMS_TO_COMPUTE[:batch_size]  # Create a list based on batch size
    GLOBAL_NUMS_TO_COMPUTE = GLOBAL_NUMS_TO_COMPUTE[batch_size:]
    finished = (GLOBAL_NUMS_TO_COMPUTE == [])  # True if DB is empty, False if otherwise

    json_response = {
        'algorithm_to_use': algorithm_to_use,
        'numbers_to_compute': numbers_to_compute,
        'finished': finished
    }

    return json_response'''


def get_json_response(batch_size=100):
    records = retrieve_items(batch_size, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    insert_items(records, table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    delete_items(records, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

    algorithm_to_use = 'carm3'
    finished = (len(records) == 0)

    json_response = {
        'algorithm_to_use': algorithm_to_use,
        'numbers_to_compute': [record[0] for record in records],
        'finished': finished
    }

    return json_response


@app.route('/get_workload', methods=['GET'])
def get_workload():
    batch_size = int(request.args.get('batch_size'))
    if batch_size==None:
        batch_size = 100
    json_response = get_json_response(batch_size)
    print(batch_size)
    return json_response

@app.route('/send_results', methods=['POST'])
def send_results():
    #global GLOBAL_RESULTS
    # TODO: store the results in the results DB

    # TODO: remove the computed numbers from the worker queue DB
    # remove the computed numbers from current_workload_list

    print('====Got Results====')
    print(request.json['result'])
    #GLOBAL_RESULTS = GLOBAL_RESULTS + request.json['result']
    #print(GLOBAL_RESULTS)
    print('==== ====')

    # TODO: Insert results in DB
    insert_results(request.json['result'], table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    return 'False'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
