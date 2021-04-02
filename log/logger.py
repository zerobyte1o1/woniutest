#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time

from training.class43.CBT.woniutest.common.common import Project


class Logger:

    logger = None

    # 利用单例模式构造logger的实例
    @classmethod
    def get_logger(cls):
        if cls.logger is None:
            log_path = Project.get_resource_path('log')
            now = int(time.time())
            log_file = os.path.join(log_path, f'woniutest_{now}.log')
            # 构造日志对象前必须先进行一些配置
            logging.basicConfig(
                level=logging.INFO,
                format='[%(asctime)s] %(levelname)s %(filename)s: %(lineno)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                handlers=[logging.FileHandler(log_file, encoding='utf8'), logging.StreamHandler()]
            )
            # 获得logger的实例化对象
            cls.logger = logging.getLogger()
        return cls.logger

