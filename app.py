from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(message="Hello from Sparki Flask app")


@app.route('/health')
def health():
    return jsonify(status="ok")


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json(silent=True)
    return jsonify(received=data)


if __name__ == '__main__':
    # Runs on localhost:5000 by default
    app.run(host='127.0.0.1', port=5000, debug=True)
