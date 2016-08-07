# Created by wushuyi on 2016/8/5 0005.
from flask import Flask, request, jsonify, \
    send_from_directory, send_file
from flask_cors import CORS
from viewer import FileManagerView

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return send_file('./index.html')


# app.add_url_rule

@app.route('/manager/<path:path>')
def send_manager(path):
    return send_from_directory('./Filemanager-2.4.0', path)


@app.route('/tinymce_4.4.1/<path:path>')
def send_tinymce(path):
    return send_from_directory('./tinymce_4.4.1', path)


@app.route('/userfiles/<path:path>')
def send_userfiles(path):
    return send_from_directory('/home/wushuyi/userfiles', path)


app.add_url_rule('/filemanager', view_func=FileManagerView.as_view('manager'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
