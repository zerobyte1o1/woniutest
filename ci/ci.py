#! /usr/bin/env python
# -*- coding: utf-8 -*-

from training.class43.CBT.woniutest.log.logger import Logger
import os
import time


class CI:

    def __init__(self):
        self.logger = Logger.get_logger()

    def checkout(self):
        if os.path.exists('./woniusales'):
            os.system('git -C woniusales pull origin master')
        else:
            os.system('git clone ssh://git@xawn.f3322.net:1122/jacky/woniusales.git')
        self.logger.info('从代码仓库获取项目代码。')
        time.sleep(3)

    def build(self):
        os.system('ant -f woniusales/build.xml')
        self.logger.info('构建项目可执行程序包。')
        time.sleep(5)

    def deploy(self):
        os.system('echo y | pscp -pw jackywang woniusales/woniusales.war'
                  ' root@172.16.11.32:/usr/local/apache-tomcat-8.5.42/webapps/')
        self.logger.info('将项目可执行程序包部署到测试环境中。')
        time.sleep(15)

    def start(self):
        self.checkout()
        self.build()
        self.deploy()
