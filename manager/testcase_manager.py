#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import time

from training.class43.CBT.woniutest.ci.ci import CI
from training.class43.CBT.woniutest.common.common import BrowserDriver
from training.class43.CBT.woniutest.action.api_action import HttpAction
from training.class43.CBT.woniutest.action.ui_action import UiAction
from training.class43.CBT.woniutest.common.common import Project, HttpSession
from training.class43.CBT.woniutest.common.report import Reporter
from training.class43.CBT.woniutest.log.logger import Logger
from training.class43.CBT.woniutest.read_data.read_script import ReadScript


class TestcaseManager:

    def __init__(self, version):
        self.version = version
        self.reporter = Reporter(version)
        self.logger = Logger.get_logger()

    def discovery(self, rule):
        testcase_path = Project.get_resource_path('testcase')
        # 利用glob模块的glob方法来获取指定规则路径下的文件，其返回结果是一个列表类型的数据
        return glob.glob(os.path.join(testcase_path, rule))

    def run(self, host, *args):
        for path in args:
            test_type = '接口测试' if 'api' in path else 'UI测试'
            if test_type == '接口测试':
                with HttpSession() as session:
                    action = HttpAction(session, host)
                    self.test(action, test_type, path)
            else:
                with BrowserDriver() as driver:
                    action = UiAction(driver, host)
                    self.test(action, test_type, path)

    def test(self, action, test_type, path):
        rs = ReadScript(path)
        # 为接口测试定义一个可以保存请求返回值的变量备用
        resp = None
        try:
            for line in rs.scripts:
                method_name = line.pop(0).lower().replace(' ', '_')
                if hasattr(action, method_name):
                    if test_type == '接口测试':
                        # 针对HttpAction中的方法，断言没有返回值，请求有返回值这样的特点进行分别处理
                        if 'should' in method_name:
                            # 分别获取自己定义的响应提取类型、期望结果
                            response_type = line.pop(0)
                            expected = line.pop(0)
                            # 利用HttpAction实现的提取响应内容的方法获取要进行断言的具体实测数据
                            actual = action.get_actual(resp, response_type)
                            getattr(action, method_name)(actual, expected)
                        else:
                            # 分别获取请求路径，请求的数据
                            uri = line.pop(0)
                            # 对于请求数据进行构造，这里是将键值对构造为字典
                            data = rs.map2json(line.pop(0))
                            resp = getattr(action, method_name)(uri, data=data)
                    else:
                        getattr(action, method_name)(*line)
            self.reporter.write_report(rs.module, test_type, rs.title, '成功', '无', '无')
            self.logger.info(f'{test_type}: {rs.module}模块测试用例{rs.title}测试成功。')
        except AssertionError as e:
            screenshot = self.capture_screen(action, test_type)
            self.reporter.write_report(rs.module, test_type, rs.title, '失败', str(e), screenshot)
            self.logger.info(f'{test_type}: {rs.module}模块测试用例'
                             f'{rs.title}测试遇到断言错误。错误原因：{str(e)}。')
        except Exception as e:
            screenshot = self.capture_screen(action, test_type)
            self.reporter.write_report(rs.module, test_type, rs.title, '错误', str(e), screenshot)
            self.logger.info(f'{test_type}: {rs.module}模块测试用例'
                             f'{rs.title}测试遇到意外错误。错误原因：{str(e)}。')

    def capture_screen(self, action, test_type):
        if test_type == 'UI测试':
            now = int(time.time())
            return action.capture_screen(f'{self.version}_{now}.png')
        return '无'

    def query_report(self):
        self.reporter.build_report()
        attachment = self.reporter.compress_report()
        # self.reporter.send_report(attachment)


if __name__ == '__main__':
    host = 'http://xawn.f3322.net:8060/woniusales'
    ci = CI().start()
    manager = TestcaseManager('0.0.7')
    cases = manager.discovery('*')
    manager.run(host, *cases)
    manager.query_report()
