#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import matplotlib.pyplot as plot

from performance.jdbc import query_column
from performance.utils import img_path
from config import CF


class GraphsPlot(object):
    def __init__(self, dbname):
        self.dbname = dbname

    def font(self):
        """字体"""
        if 'win' in sys.platform:
            plot.rcParams['font.sans-serif'] = ['Songti SC']  # 用来正常显示中文标签
        else:
            plot.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def picture(self, column, ylim, ylabel, color):
        """
        plot基础图
        :param col: 列名
        :param ylim: Y轴最大值
        :param ylabel: Y轴名称
        :return:
        """
        y = query_column(column, self.dbname)
        plot.xlim((0, len(y)))  # X轴界限
        plot.ylim((1, ylim))  # Y轴界限
        plot.xlabel('time axis')
        plot.ylabel(ylabel)
        plot.plot(range(len(y)), y, color, label=f'{column}{CF.CSV_TITLE_EN[column]}')
        plot.legend()

    def graphical(self, column, ylim, ylabel, color='b'):
        """绘制一张图"""
        self.font()
        plot.figure(dpi=128)
        plot.title(CF.CSV_TITLE_EN[column])
        self.picture(column, ylim, ylabel, color)
        plot.savefig(img_path(CF.CSV_TITLE_EN[column]))
        plot.show()

    def graphics(self):
        """生成四个图"""
        self.font()
        plot.figure(figsize=(10, 6), dpi=128)
        pref_info = [
            ('CPU', 100, '%', 'm'),
            ("FPS", 100, "FPS", 'y'),
            ('memory', 4096, 'MB', 'b'),
            ('Delay_ratio', 100, '%', 'g')
        ]
        for index, value in enumerate(pref_info):
            index += 1
            plot.subplot(2, 2, index)
            self.picture(*value)
        plot.tight_layout()
        plot.show()


if __name__ == '__main__':
    plots = GraphsPlot('ipal')
    # plots.graphics()
    plots.graphical('CPU', 100, '%', 'm')
