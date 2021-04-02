#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

from training.class43.CBT.woniutest.common.common import Project


class ReadScript:

    def __init__(self, path):
        # count在这里用来记录方法递归的次数
        self.count = 0
        self._scripts = self.__reader__(path)

    # 方法自己调用自己的方式叫做递归算法
    def __reader__(self, path):
        if not os.path.exists(path) or os.path.isdir(path):
            return None
        scripts = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # 在这里检查方法的递归层数，如果是第一层，那么执行获取模块名与测试用例标题的动作；
            # 如果不是第一层，这里仅做向下滚行的操作
            if self.count == 0:
                # 利用迭代器对象的__next__方法从迭代器中提取一个数据（注意这里实际上就是提取一行）
                self._module, self._title = reader.__next__()
            else:
                reader.__next__()
            # 递归层次计数器累加计数行为
            self.count += 1
            for line in reader:
                if line[0].endswith('.txt'):
                    subcase_path = os.path.join(os.path.dirname(path), line[0])
                    # 利用递归算法来处理脚本中存在嵌套的情况，确保无论是否有嵌套都可以准确获得脚本行内容
                    # 列表元素如何添加列表元素的方法
                    scripts.extend(self.__reader__(subcase_path))
                else:
                    scripts.append(line)
        return scripts

    @property
    def scripts(self):
        if self._scripts is None:
            raise FileExistsError
        return self._scripts

    @property
    def module(self):
        return self._module

    @property
    def title(self):
        return self._title

    # 针对测试脚本中的键值对数据提供将其解析为字典的方法
    @staticmethod
    def map2json(map_data):
        dict_data = {}
        for item in map_data.split('&'):
            key, value = item.split('=')
            dict_data[key] = value
        return dict_data


if __name__ == '__main__':
    rs = ReadScript(os.path.join(Project.get_resource_path('testcase'), 'test_ui_login.txt'))
    print(rs.module, rs.title)
    print(rs.scripts)
