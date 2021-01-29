import os
import sys

WIN = sys.platform.startswith('win')

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True

PREFIX = 'sqlite:///' if WIN else 'sqlite:////'
SQLALCHEMY_DATABASE_URI = PREFIX + os.path.join(BASE_DIR, 'data.db')

PAGE_SIZE = 15

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload')
ALLOWED_EXTENSIONS = {'csv'}


if __name__ == '__main__':
    print(BASE_DIR)
