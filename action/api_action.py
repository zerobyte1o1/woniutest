#! /usr/bin/env python
# -*- coding: utf-8 -*-

import jsonpath

from training.class43.CBT.woniutest.log.logger import Logger


class HttpAction:

    def __init__(self, session, host):
        self.session = session
        self.host = host
        self.logger = Logger.get_logger()

    def get(self, uri, **kwargs):
        resp = self.session.get(self.host + uri, **kwargs)
        self.logger.info(f'发送GET请求: url={resp.request.url}，收到的响应代码：{resp.status_code}。')
        return resp

    def post(self, uri, data=None, json=None, **kwargs):
        resp = self.session.post(self.host + uri, data, json, **kwargs)
        self.logger.info(f'发送POST请求：url={resp.request.url}, headers={resp.request.headers},'
                         f' body={resp.request.body}，收到的响应代码：{resp.status_code}。')
        return resp

    def put(self, uri, data=None, **kwargs):
        resp = self.session.put(self.host + uri, data, **kwargs)
        return resp

    def delete(self, uri, **kwargs):
        resp = self.session.delete(self.host + uri, **kwargs)
        return resp

    def status_should_be(self, actual, expected):
        assert actual == int(expected), f'断言错误：返回的响应代码{actual}不等于期望值{expected}。'

    def should_be_equal(self, actual, expected):
        assert actual == expected, f'断言错误：响应返回的内容{actual}不等于期望值{expected}。'

    # 定义一个针对接口响应内容，按照测试脚本指定的处理去提取实测结果的方法
    def get_actual(self, response, response_type):
        # 注意目前版本只定义实现了三种结果提取类型，但是使用的时候可以依据具体的项目自己再行扩展
        if response_type == 'code':
            return response.status_code
        elif response_type == 'text':
            return response.text
        elif 'jsonpath' in response_type:
            resp_json = response.json()
            response_type = response_type.replace('jsonpath', '')
            # 利用jsonpath模块的jsonpath方法来提取需要的值
            # jsonpath.jsonpath(json数据，jsonpath表达式)，返回一个列表类型的值。
            return jsonpath.jsonpath(resp_json, response_type)[0]
        else:
            # 对于未定义的类型抛出错误，避免测试时候的测试行为失败
            raise TypeError
