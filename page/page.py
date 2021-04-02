#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait


class Page:

    def __init__(self, driver):
        self.driver = driver

    # 计划传入的locator样式如下：
    # locator: id=username
    def get_element(self, locator):
        # 这里为了灵活调用定位方法，所以调用了一个相对底层定位方法
        return self.driver.find_element(*self.get_locator(locator))

    def wait_until_element(self, locator, timeout):
        # 显示等待的简单方法实现
        # for _ in range(timeout):
        #     try:
        #         self.get_element(locator)
        #         return True
        #     except Exception:
        #         time.sleep(1)
        # return False
        # 显示等待selenium提供的方法实现
        try:
            WebDriverWait(self.driver, timeout).\
                until(lambda dr: dr.find_element(*self.get_locator(locator)))
            return True
        except TimeoutException:
            return False

    def element_is_exists(self, locator):
        return self.wait_until_element(locator, 5)

    # 注意传入的locator形式如下：
    # id=username
    # 返回的结果是(id, username)
    def get_locator(self, locator):
        by, value = locator.lower().split('=', 1)
        if by == By.ID or by == By.XPATH or by == By.NAME:
            return by, value
        elif by == By.LINK_TEXT or by == By.LINK_TEXT.split(' ')[0]:
            return By.LINK_TEXT, value
        elif by == By.PARTIAL_LINK_TEXT or by == By.PARTIAL_LINK_TEXT.split(' ')[0]:
            return By.PARTIAL_LINK_TEXT, value
        elif by == By.TAG_NAME or by == By.TAG_NAME.split(' ')[0]:
            return By.TAG_NAME, value
        elif by == By.CLASS_NAME or by == By.CLASS_NAME.split(' ')[0]:
            return By.CLASS_NAME, value
        elif by == By.CSS_SELECTOR or by == By.CSS_SELECTOR.split(' ')[0]:
            return By.CSS_SELECTOR, value
        else:
            raise NoSuchElementException
