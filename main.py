#!/usr/bin/env python3
# coding=utf-8
import unittest
from performance.utils import adb_pull
from performance.graphs import GraphsPlot
from performance.readcsv import read_csv_db


## 你好
class TestPlot(unittest.TestCase):
    """绘制所有的对比图"""

    @classmethod
    def setUpClass(cls) -> None:
        adb_pull()
        cls.dbname = 'ipal'  # 数据库名称
        read_csv_db(cls.dbname)
        cls.graphs = GraphsPlot(cls.dbname)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_001(self):
        """全局占用_CPU"""
        self.graphs.graphical('CPU', 100, '%')

    def test_002(self):
        """全局内存占用"""
        self.graphs.graphical('memory', 4096, 'MB')

    def test_003(self):
        """FPS帧率刷新"""
        self.graphs.graphical('FPS', 80, 'FPS')

    def test_004(self):
        """平均电流"""
        self.graphs.graphical('average_battery', -1000, 'mA')

    def test_005(self):
        """实时电流"""
        self.graphs.graphical('Real_time_battery', -1500, 'mA')

    def test_006(self):
        """刷新耗时"""
        self.graphs.graphical('refresh_time_consuming', 50000, 'ms')

    def test_007(self):
        """响应耗时"""
        self.graphs.graphical('response_time_consuming', 1500, 'ms')

    def test_008(self):
        """延迟次数"""
        self.graphs.graphical('Delay_times', 50, 'number of times')

    def test_009(self):
        """延迟占比"""
        self.graphs.graphical('Delay_ratio', 100, '%')

    def test_010(self):
        """最大延迟时间"""
        self.graphs.graphical('Maximum_delay_time', 500, 'ms')

    def test_011(self):
        """累积应用上行流量"""
        self.graphs.graphical('app_uplink', 200, 'KB')

    def test_012(self):
        """应用上行速率"""
        self.graphs.graphical('app_uplink_speed', 50, 'KB')

    def test_013(self):
        """累计应用下行流量"""
        self.graphs.graphical('app_downlink', 10000, 'KB')

    def test_014(self):
        """应用下行速率"""
        self.graphs.graphical('app_downlink_speed', 2000, 'KB')

    def test_015(self):
        """PSS内存-appbrand0-3030"""
        self.graphs.graphical('PSS', 800, 'MB')


if __name__ == '__main__':
    unittest.main(verbosity=2)
