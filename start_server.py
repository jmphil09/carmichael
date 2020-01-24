from datetime import datetime
from flask import Flask, request

from db_commands import insert_items, delete_items, retrieve_items, insert_results


#TODO: Put these values in a config file
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'numbers_to_compute'
DATABASE_RESULTS = 'results'

#TODO: Add docstrings

app = Flask(__name__)


def get_json_response(batch_size=100):
    records = retrieve_items(batch_size, table='numbers_to_compute', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    insert_items(records, table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    insert_items(records, table='selected_items', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
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
    req_json = request.json['result']
    print('====Got Results====')
    print(req_json)
    print('==== ====')
    # Insert results in DB
    result_date = str(datetime.now())
    result_host = request.headers['Host']
    db_results = [(r[0], r[1], r[2], r[3], result_host, result_date) for r in req_json]
    items_to_delete = [(r[0], r[3]) for r in req_json]
    insert_results(db_results, table='results', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    delete_items(items_to_delete, table='computing_table', user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    return 'False'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
