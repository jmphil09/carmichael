from flask import Flask

app = Flask(__name__)


def get_json_response():
    return {
        "algorithm_to_use": "carm3",
        "numbers_to_compute": (3, 10000, 1)
    }

@app.route('/')
def example():
    json_response = get_json_response()
    return json_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
