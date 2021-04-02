#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import ImageGrab
import cv2
import os

from training.class43.CBT.woniutest.common.common import Project


class ImageMatch:

    def find_image(self, target):
        base_path = Project.get_resource_path('image')
        screen_path = os.path.join(base_path, 'screen.png')
        ImageGrab.grab().save(screen_path)
        screen = cv2.imread(screen_path)
        template = cv2.imread(os.path.join(base_path, target))
        # 利用opencv的matchTemplate方法进行图像识别
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        # 利用opencv的minMaxLoc方法获取匹配度和匹配位置
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        similarity = max_value
        if similarity < 0.95:
            return -1, -1
        pos_x = max_loc[0] + int(template.shape[1] / 2)
        pos_y = max_loc[1] + int(template.shape[0] / 2)
        return pos_x, pos_y

    # 定义一个检查指定模板图片是否存在的方法。用于断言
    def check_exists(self, target):
        x, y = self.find_image(target)
        return x != -1 and y != -1
