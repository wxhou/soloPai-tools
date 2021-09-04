import time
import uuid
from pypinyin import lazy_pinyin
from flask import current_app


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def pathname(mat="%Y%m%d"):
    return str(time.strftime(mat, time.localtime()))


def to_pinyin(filename):
    return "".join(lazy_pinyin(filename))
