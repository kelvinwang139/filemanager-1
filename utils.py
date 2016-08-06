# Created by wushuyi on 2016/8/5 0005.
from werkzeug.utils import secure_filename
from flask import request, send_file
import os
from PIL import Image

path_exists = os.path.exists
normalize_path = os.path.normpath
absolute_path = os.path.abspath
split_path = os.path.split
split_ext = os.path.splitext

UPLOAD_FOLDER = '/home/wushuyi/userfiles'
ROOT_FOLDER = '/home/wushuyi'
SERVICE_PATH = "http://192.168.0.107:5000"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def addfile(file=None, currentpath=None):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(ROOT_FOLDER + currentpath, filename))
        return filename


def getinfo(path=None, getsize=True, req=None):
    """Returns a JSON object containing information about the given file."""

    thefile = {
        'Filename': split_path(path)[-1],
        'File Type': '',
        # 'Preview': path.split(ROOT_FOLDER)[1] if split_path(path)[-1] else 'images/fileicons/_Open.png',
        'Preview': 'images/fileicons/_Open.png' if os.path.isdir(path) else path.split(ROOT_FOLDER)[1],
        'Path': path.split(ROOT_FOLDER)[1],
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

    if not path_exists(path):
        thefile['Error'] = 'File does not exist.'
        return thefile

    if os.path.isdir(path):
        thefile['File Type'] = 'dir'

        if thefile['Path'][-1] != '/':
            thefile['Path'] += '/'

    else:
        thefile['File Type'] = ext = split_ext(path)[1][1:]

        if ext in imagetypes:
            img = Image.open(path)
            thefile['Properties']['Width'] = img.width
            thefile['Properties']['Height'] = img.height

        else:
            previewPath = 'images/fileicons/' + ext.upper + '.png'
            thefile['Preview'] = previewPath if path_exists('../../' + previewPath) else 'images/fileicons/default.png'

        thefile['Properties']['Date Created'] = os.path.getctime(path)
        thefile['Properties']['Date Modified'] = os.path.getmtime(path)
        if getsize:
            thefile['Properties']['Size'] = os.path.getsize(path)
        thefile['Preview'] = SERVICE_PATH + thefile['Preview']

    return thefile


def getfolder(path=None, getsizes=True, req=None):
    result = {}
    filelist = os.listdir(path)
    for i in filelist:
        file = os.path.join(path, i)
        res = getinfo(path=file, getsize=getsizes)
        result[res['Path']] = res
    return result


def rename(old=None, new=None, req=None):
    if old[-1] == '/':
        old = old[:-1]

    oldname = os.path.basename(old)
    path = os.path.split(old)[0]
    if not path[-1] == '/':
        path += '/'

    newname = secure_filename(new)
    newpath = path + newname

    os.rename(ROOT_FOLDER + old, ROOT_FOLDER + newpath)

    result = {
        'Code': 0,
        'Old Path': old,
        'Old Name': oldname,
        'New Path': newpath,
        'New Name': newname,
        'Error': 'There was an error renaming the file.'
    }

    return result


def delete(path=None, req=None):
    if os.path.isdir(ROOT_FOLDER + path):
        os.removedirs(ROOT_FOLDER + path)
    else:
        os.remove(ROOT_FOLDER + path)

    result = {
        'Code': 0,
        'Path': path,
        'Error': ''
    }
    return result


def addfolder(path=None, name=None):
    newName = secure_filename(name)
    newPath = ROOT_FOLDER + path + newName + '/'

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


def download(path=None, req=None):
    name = os.path.basename(path)

    return send_file(filename_or_fp=ROOT_FOLDER + path,
                     attachment_filename=name)
