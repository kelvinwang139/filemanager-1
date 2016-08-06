# Created by wushuyi on 2016/8/5 0005.
from flask import Flask, request, jsonify, \
    send_from_directory
from flask_cors import CORS, cross_origin
from utils import addfile, getfolder, getinfo, rename, delete, \
    addfolder, download
import os

BASE_FOLDER = '/home/wushuyi'
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    # return 'Hello World!'
    res = getfolder(path='/home/wushuyi/userfiles')
    return jsonify(res)


@app.route('/manager/<path:path>')
def send_manager(path):
    return send_from_directory('./Filemanager-2.4.0', path)


@app.route('/userfiles/<path:path>')
def send_userfiles(path):
    return send_from_directory('/home/wushuyi/userfiles', path)


@app.route('/filemanager', methods=['POST', 'GET'])
def filemanager():
    if request.method == 'GET':
        mode = request.args.get('mode')
        if mode == 'getinfo':
            path = request.args.get('path')
            config = request.args.get('config')
            time = request.args.get('time')
            # print(os.path.join(BASE_FOLDER, path))
            res = getinfo(path=(BASE_FOLDER + path))
            return jsonify(res)
        if mode == 'getfolder':
            path = request.args.get('path')
            config = request.args.get('config')
            showThumbs = request.args.get('showThumbs')
            time = request.args.get('time')
            res = getfolder(path=(BASE_FOLDER + path))
            return jsonify(res)
        if mode == 'rename':
            old = request.args.get('old')
            new = request.args.get('new')
            config = request.args.get('config')
            res = rename(old=old, new=new)
            return jsonify(res)
        if mode == 'delete':
            path = request.args.get('path')
            config = request.args.get('config')
            time = request.args.get('time')
            res = delete(path=path)
            return jsonify(res)
        if mode == 'addfolder':
            path = request.args.get('path')
            config = request.args.get('config')
            name = request.args.get('name')
            time = request.args.get('time')
            res = addfolder(path=path, name=name)
            return jsonify(res)
        if mode == 'download':
            path = request.args.get('path')
            config = request.args.get('config')
            return download(path=path)
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'add':
            file = request.files.get('newfile')
            config = request.args.get('config')
            currentpath = request.form.get('currentpath')
            filename = addfile(file=file, currentpath=currentpath)
            return '<textarea>{"Path":"' + currentpath + '","Name":"' + filename + '","Error":"","Code":0}</textarea>'
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
