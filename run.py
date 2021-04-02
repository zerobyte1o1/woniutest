#! /usr/bin/env python
# -*- coding: utf-8 -*-
from training.class43.CBT.woniutest.ci.ci import CI
from training.class43.CBT.woniutest.manager.testcase_manager import TestcaseManager

if __name__ == '__main__':
    host = 'http://xawn.f3322.net:8060/woniusales'
    ci = CI().start()
    manager = TestcaseManager('0.0.7')
    cases = manager.discovery('*')
    manager.run(host, *cases)
    manager.query_report()
