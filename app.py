import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__, static_folder='build/', static_url_path='/')
CORS(app)
app.debug = 'DEBUG' in os.environ

@app.route('/upload', methods=['GET', 'POST'])
def uploadNotes():
    print(request)
    print(request.form)
    print(request.form.get('title'))
    print(request.form.items())
    for key, val in request.form.items():
        print(key)
        print(val)
    if('file' not in request.files):
        print("oh no")
    else:
        f = request.files['file']
        print("oh yes")
        print(f.filename)
        print(type(f))
    print(len(request.form))
    return "Completed"

@app.route('/')
def index():
    return app.send_static_file('index.html')


if(__name__ == '__main__'):
    print('server name ', app.config["SERVER_NAME"])
    app.run(debug=True)
