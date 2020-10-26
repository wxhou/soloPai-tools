#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import csv
from pprint import pprint
from itertools import islice

from config import CF
from performance.jdbc import SQLite, create_table
from performance.utils import csv_names, get_new_records

__all__ = ['read_csv_db']


def read_csv_db(dbname):
    """将CSV中的数据存至数据库"""
    csv_contents = [(csv_name, config_name) for csv_name in csv_names(get_new_records())
                    for config_name in CF.CSV_TITLE_CN if config_name in csv_name]
    print(csv_contents)
    create_table(dbname)
    for csv_name, config_name in csv_contents:
        with open(csv_name, 'r', encoding='GB2312') as f:
            csv_data = list(csv.reader(f))
        with SQLite() as cur:
            for i in islice(enumerate(csv_data), 1, None):
                for row_num in range(1, len(csv_data)):
                    cur.execute("insert or ignore into %s(id) values (?);" % dbname, (row_num,))
                print(CF.CSV_TITLE_CN[config_name], i[1][1], i[0])
                cur.execute("update %s set %s=? where id=?;" % (dbname, CF.CSV_TITLE_CN[config_name]), (i[1][1], i[0]))


if __name__ == "__main__":
    print(read_csv_db('ipal'))
