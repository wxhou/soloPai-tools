import os
import time
from config import CF
from pprint import pprint


def adb_pull():
    r = os.popen('adb pull -p -a /sdcard/solopi/records/ %s' % CF.BASE_DIR)
    print(r.read())


def get_new_records():
    def realpath(i): return os.path.join(CF.RECORDS_DIR, i)

    result = [i for i in os.listdir(CF.RECORDS_DIR)
              if os.path.isdir(realpath(i))]
    pathname = sorted(result, key=lambda x: os.path.getctime(realpath(x)))[0]
    return pathname


def csv_names(name):
    _path = os.path.join(CF.RECORDS_DIR, name)
    analysis = [os.path.join(root, filename) for root, _, files in os.walk(_path)
                for filename in files if filename.endswith('.csv')]
    return sorted(analysis, reverse=True)


def img_path(name):
    timestamp = time.time()
    if not os.path.exists(CF.IMAGES_DIR):
        os.makedirs(CF.IMAGES_DIR)
    return os.path.join(CF.IMAGES_DIR, "{}{}.png".format(int(timestamp), name))


if __name__ == "__main__":
    pprint(get_new_records())
