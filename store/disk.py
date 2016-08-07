# Created by wushuyi on 2016/8/7 0007.
import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import send_file


class FileManager(object):
    def __init__(self, config=None):
        self.cfg = config

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.cfg.ALLOWED_EXTENSIONS

    def addfile(self, file=None, currentpath=None):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.cfg.ROOT_FOLDER + currentpath, filename))
            return filename

    def getinfo(self, path=None, getsize=True):
        """Returns a JSON object containing information about the given file."""
        if path.find(self.cfg.ROOT_FOLDER) == -1:
            path = self.cfg.ROOT_FOLDER + path
        thefile = {
            'Filename': os.path.split(path)[-1],
            'File Type': '',
            'Preview': 'images/fileicons/_Open.png' if os.path.isdir(path) else path.split(self.cfg.ROOT_FOLDER)[1],
            'Path': path.split(self.cfg.ROOT_FOLDER)[1],
            'Error': '',
            'Code': 0,
            'Properties': {
                'Date Created': None,
                'Date Modified': None,
                'Width': None,
                'Height': None,
                'Size': None
            }
        }

        imagetypes = ('gif', 'jpg', 'jpeg', 'png')

        if not os.path.exists(path):
            thefile['Error'] = 'File does not exist.'
            return thefile

        if os.path.isdir(path):
            thefile['File Type'] = 'dir'

            if thefile['Path'][-1] != '/':
                thefile['Path'] += '/'

        else:
            thefile['File Type'] = ext = os.path.splitext(path)[1][1:]

            if ext in imagetypes:
                img = Image.open(path)
                thefile['Properties']['Width'] = img.width
                thefile['Properties']['Height'] = img.height

            else:
                previewPath = 'images/fileicons/' + ext.upper + '.png'
                thefile['Preview'] = previewPath if os.path.exists(
                    '../../' + previewPath) else 'images/fileicons/default.png'

            thefile['Properties']['Date Created'] = os.path.getctime(path)
            thefile['Properties']['Date Modified'] = os.path.getmtime(path)
            if getsize:
                thefile['Properties']['Size'] = os.path.getsize(path)
            thefile['Preview'] = self.cfg.SERVICE_PATH + thefile['Preview']

        return thefile

    def getfolder(self, path=None, getsizes=True):
        path = self.cfg.ROOT_FOLDER + path
        result = {}
        filelist = os.listdir(path)
        for i in filelist:
            file = os.path.join(path, i)
            res = self.getinfo(path=file, getsize=getsizes)
            result[res['Path']] = res
        return result

    def rename(self, old=None, new=None, req=None):
        if old[-1] == '/':
            old = old[:-1]

        oldname = os.path.basename(old)
        path = os.path.split(old)[0]
        if not path[-1] == '/':
            path += '/'

        newname = secure_filename(new)
        newpath = path + newname

        os.rename(self.cfg.ROOT_FOLDER + old, self.cfg.ROOT_FOLDER + newpath)

        result = {
            'Code': 0,
            'Old Path': old,
            'Old Name': oldname,
            'New Path': newpath,
            'New Name': newname,
            'Error': 'There was an error renaming the file.'
        }

        return result

    def delete(self, path=None, req=None):
        if os.path.isdir(self.cfg.ROOT_FOLDER + path):
            os.removedirs(self.cfg.ROOT_FOLDER + path)
        else:
            os.remove(self.cfg.ROOT_FOLDER + path)

        result = {
            'Code': 0,
            'Path': path,
            'Error': ''
        }
        return result

    def addfolder(self, path=None, name=None):
        newName = secure_filename(name)
        newPath = self.cfg.ROOT_FOLDER + path + newName + '/'

        if not os.path.exists(newPath):
            try:
                os.mkdir(newPath)
                result = {'Code': 0,
                          'Error': '',
                          'Name': newName,
                          'Parent': path
                          }
            except:
                result = {
                    'Parent': path,
                    'Name': newName,
                    'Error': 'There was an error creating the directory.'  # TODO grab the actual traceback.
                }
        return result

    def download(self, path=None, req=None):
        name = os.path.basename(path)

        return send_file(filename_or_fp=self.cfg.ROOT_FOLDER + path,
                         attachment_filename=name,
                         as_attachment=True)
