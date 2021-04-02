#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

from selenium.common.exceptions import NoSuchElementException
from pymouse import PyMouse
from pykeyboard import PyKeyboard

from training.class43.CBT.woniutest.common.image_match import ImageMatch
from training.class43.CBT.woniutest.common.common import Project
from training.class43.CBT.woniutest.log.logger import Logger
from training.class43.CBT.woniutest.page.page import Page


class UiAction:

    def __init__(self, driver, host):
        self.driver = driver
        self.host = host
        self.page = Page(driver)
        self.logger = Logger.get_logger()
        self.match = ImageMatch()
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

    def open_browser(self, uri):
        # 注意：一定要把项目的host部分独立出来，方便未来测试的时候切换环境
        url = self.host + uri
        self.driver.get(url)
        self.logger.info(f'打开浏览器访问被测网站{url}。')

    def input_text(self, locator, content):
        element = self.page.get_element(locator)
        element.clear()
        element.send_keys(content)
        self.logger.info(f'在{locator}元素上输入{content}。')

    def input_password(self, locator, password):
        self.input_text(locator, password)

    def click_element(self, locator):
        self.page.get_element(locator).click()
        self.logger.info(f'在{locator}元素上单击一次。')

    def set_implicitly_wait(self, timeout):
        self.driver.implicitly_wait(timeout)
        self.logger.info(f'设置全局隐式等待时间为{timeout}秒。')

    def wait_until_element_contains(self, locator, content, timeout=5):
        # 针对指定的元素进行等待，如果等待成功，那么获得该元素对象，并去按指定条件进行检查，
        # 满足则返回True；不满足，则返回Flase。
        if self.page.wait_until_element(locator, float(timeout)):
            self.logger.info(f'等待元素{locator}包含{content}内容出现。')
            return content in self.page.get_element(locator).text
        self.logger.warn(f'没有等到指定{locator}元素。')
        return False

    def input_text_by_template(self, target, content):
        x, y = self.click_by_template(target)
        self.keyboard.type_string(str(content))
        self.logger.info(f'在指定元素{target}对象中输入{content}。')

    def click_by_template(self, target):
        x, y = self.match.find_image(target)
        if x == -1 or y == -1:
            self.logger.error(f'没有找到指定的元素{target}对象。')
            raise NoSuchElementException
        self.mouse.click(x, y)
        self.logger.info(f'在指定元素{target}对象上单击。')
        return x, y

    def capture_screen(self, filename):
        # 构造截图的默认路径
        screen_path = Project.get_resource_path('report/screenshot')
        self.driver.get_screenshot_as_file(os.path.join(screen_path, filename))
        self.logger.info(f'截取当前画面并保存为文件{filename}。')
        # 注意这里返回的是图片文件的相对路径
        return f'screenshot/{filename}'

    def element_should_contains(self, locator, expected):
        # 这里利用了python内置的断言语句assert，该语句的用法如下：
        # assert conditional, error_message
        # conditional表示条件，其值必须是布尔类型
        # error_message是当断言错误时会显示的消息
        # 在一个方法中有多个断言语句assert的时候，那么多个语句的关系是逻辑与的关系。
        assert self.page.element_is_exists(locator), f'断言错误：指定的元素{locator}对象没找到。'
        actual = self.page.get_element(locator).text
        assert expected in actual, f'断言错误：实际测试结果{actual}中不包含预期的值{expected}。'
