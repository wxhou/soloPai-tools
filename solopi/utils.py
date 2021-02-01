import time
from pypinyin import lazy_pinyin
from flask import current_app
from .models import SoloPiTag


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def pathname(mat="%Y%m%d%H%M%S"):
    return str(time.strftime(mat, time.localtime()))


def to_pinyin(filename):
    return "".join(lazy_pinyin(filename))
