import os
import json
import backend
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__, static_folder='build/', static_url_path='/')
CORS(app)
app.debug = 'DEBUG' in os.environ

@app.route('/upload', methods=['POST'])
def uploadNotes():
    print("called")
    data = dict()

    for key, val in request.form.items():
        data[key] = val

    if('file' not in request.files):
        return { "status": "ERR_MISSING_FILE" }
    else:
        f = request.files['file']
        data['file'] = f

    print(data)
    backend.upload()

    return json.dumps({ "status": "SUCCESS" })

@app.route('/fetch', methods=['GET'])
def fetchData():
    return jsonify(backend.get_data())

@app.route('/')
def index():
    return app.send_static_file('index.html')


if(__name__ == '__main__'):
    print('server name ', app.config["SERVER_NAME"])
    app.run(debug=True)
