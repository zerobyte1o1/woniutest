#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from selenium import webdriver
import requests
import os

from training.class43.CBT.woniutest.common.db_config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_CHARSET


class BrowserDriver:

    def __init__(self, browser_type='firefox'):
        if browser_type == 'firefox' or browser_type == 'ff':
            driver_path = os.path.join(Project.get_path(), 'driver/geckodriver.exe')
            self.driver = webdriver.Firefox(executable_path=driver_path)
        elif browser_type == 'chrome' or browser_type == 'gc':
            driver_path = os.path.join(Project.get_path(), 'driver/chromedriver.exe')
            self.driver = webdriver.Chrome(executable_path=driver_path)
        else:
            driver_path = os.path.join(Project.get_path(), 'driver/IEDriverServer.exe')
            self.driver = webdriver.Ie(executable_path=driver_path)

    # 要实现with模式，那么需要覆写内置方法__enter__和__exit__
    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class HttpSession:

    def __init__(self):
        self.session = requests.session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class DbHelper:

    def __init__(self):
        self.con = pymysql.connect(host=DB_HOST, database=DB_NAME,
                                   user=DB_USER, password=DB_PASSWORD,
                                   charset=DB_CHARSET)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.cur.close()
        self.con.close()


class Project:

    # 一个类中往往有三种方法，分别是普通方法、静态方法、类方法
    # 区别：
    # 1. 参数不同。普通方法首个默认参数self，类方法首个默认参数cls，静态方法没有默认参数
    # 2. 调用方式不同。
    #   普通方法只能通过类的实例化对象来调用
    #   类方法和静态方法无需类的实例化对象，只需要类名即可调用
    # 3. 静态方法要求方法体内不可以有其所在类的任何属性或方法的调用；
    #    类方法允许在其方法体内调用其所在类的属性和方法。
    @staticmethod
    def get_path():
        return os.path.dirname(os.path.dirname(__file__))

    @classmethod
    def get_resource_path(cls, resource):
        resource_path = os.path.join(cls.get_path(), resource)
        if not os.path.exists(resource_path):
            os.makedirs(resource_path)
        return resource_path


# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.dirname(__file__)))
# driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
#                                        'driver/geckodriver.exe')
# print(driver_path)
