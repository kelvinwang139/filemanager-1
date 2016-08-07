# Created by wushuyi on 2016/8/7 0007.
from flask import request, jsonify
from flask.json import dumps as json_dumps
from flask.views import View
from store.disk import FileManager
import config


class FileManagerView(View):
    methods = ['POST', 'GET']

    def __init__(self):
        self.filemanager = FileManager(config=config)
        self.config = config

    def dispatch_request(self):
        mode = request.args.get('mode') or request.form.get('mode')
        if not mode:
            return 'arg mode must be requirst'
        func = getattr(self, mode, None)
        return func()

    def add(self):
        file = request.files.get('newfile')
        currentpath = request.form.get('currentpath')
        filename = self.filemanager.addfile(file=file, currentpath=currentpath)
        res = {
            "Path": currentpath,
            "Name": filename,
            "Error": "",
            "Code": 0
        }
        return '<textarea>' + json_dumps(res) + '</textarea>'

    def getinfo(self):
        path = request.args.get('path')
        time = request.args.get('time')
        res = self.filemanager.getinfo(path=path)
        return jsonify(res)

    def getfolder(self):
        path = request.args.get('path')
        showThumbs = request.args.get('showThumbs')
        time = request.args.get('time')
        res = self.filemanager.getfolder(path=path)
        return jsonify(res)

    def rename(self):
        old = request.args.get('old')
        new = request.args.get('new')
        res = self.filemanager.rename(old=old, new=new)
        return jsonify(res)

    def delete(self):
        path = request.args.get('path')
        res = self.filemanager.delete(path=path)
        return jsonify(res)

    def addfolder(self):
        path = request.args.get('path')
        name = request.args.get('name')
        res = self.filemanager.addfolder(path=path, name=name)
        return jsonify(res)

    def download(self):
        path = request.args.get('path')
        res = self.filemanager.download(path=path)
        return res
