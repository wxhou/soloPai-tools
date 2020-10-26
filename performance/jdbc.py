#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sqlite3
from config import CF


class SQLite(object):
    def __init__(self):
        self.con = sqlite3.connect(CF.SQLITE_DIR)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.cur.close()
        self.con.close()


def execute(sql):
    with SQLite() as cur:
        cur.execute(sql)


def query_column(column, dbname):
    with SQLite() as cur:
        cur.execute('select %s from %s;' % (column, dbname))
        return [i[0] for i in cur.fetchall()]


def create_table(name):
    create_sql = """
    CREATE TABLE IF NOT EXISTS %s(
        "id" integer PRIMARY KEY NOT NULL,
        "global_uplink" REAL,
        "global_downlink" REAL,
        "app_uplink" REAL,
        "app_downlink" REAL,
        "average_battery" REAL,
        "global_uplink_speed" REAL,
        "global_downlink_speed" REAL,
        "CPU" REAL,
        "memory" REAL,
        "Real_time_battery" REAL,
        "refresh_time_consuming" REAL,
        "response_time_consuming" REAL,
        "Delay_times" REAL,
        "Delay_ratio" REAL,
        "Application_process" REAL,
        "app_uplink_speed" REAL,
        "app_downlink_speed" REAL,
        "FPS" REAL,
        "Maximum_delay_time" REAL,
        "PrivateDirty" REAL,
        "PSS" REAL);
    """ % name
    execute(create_sql)
    print("create table '{}' done!".format(name))


if __name__ == "__main__":
    print(query_column('*', 'ipal'))
