#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import zipfile
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from training.class43.CBT.woniutest.common.common import DbHelper, Project
from training.class43.CBT.woniutest.log.logger import Logger


class Reporter:

    def __init__(self, version):
        self.version = version
        self.logger = Logger.get_logger()

    # 写入测试报告的方法
    def write_report(self, module, type, casetitle, result, error, screenshot):
        with DbHelper() as db:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            error = error.replace('"', '\\"')
            sql = f'insert into report(version, module, type, casetitle, result,' \
                  f' createtime, error, screenshot) values("{self.version}", "{module}",' \
                  f' "{type}", "{casetitle}", "{result}", "{now}", "{error}", "{screenshot}")'
            db.execute(sql)

    # 生成测试报告的方法
    def build_report(self):
        with DbHelper() as db:
            sql = f'select * from report where version = "{self.version}"'
            db.execute(sql)
            result = db.fetchall()
            if len(result) == 0:
                print(f'没有找到{self.version}版本的测试结果。')
                return
            template_path = os.path.join(Project.get_resource_path('common'), 'template.html')
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('$test_version', self.version)
            base_sql = f'select count(result) from report where version = "{self.version}" and '
            success_sql = base_sql + 'result = "成功"'
            db.execute(success_sql)
            test_success = str(db.fetchone()[0])
            content = content.replace('$test_success', test_success)
            fail_sql = base_sql + 'result = "失败"'
            db.execute(fail_sql)
            test_fail = str(db.fetchone()[0])
            content = content.replace('$test_fail', test_fail)
            error_sql = base_sql + 'result = "错误"'
            db.execute(error_sql)
            test_error = str(db.fetchone()[0])
            content = content.replace('$test_error', test_error)
            last_time_sql = f'select createtime from report where version = "{self.version}"' \
                            f' order by createtime desc limit 1'
            db.execute(last_time_sql)
            last_time = str(db.fetchone()[0])
            content = content.replace('$test_time', last_time)
            content = content.replace('$test_date', last_time.split(' ')[0])
            test_record = ''
            for index, record in enumerate(result, 1):
                if record[5] == '成功':
                    color = 'lightgreen'
                elif record[5] == '失败':
                    color = 'yellow'
                else:
                    color = 'red'
                if record[8] == '无':
                    screenshot = record[8]
                else:
                    screenshot = f'<a href="{record[8]}">查看截图</a>'
                test_record += f'<tr height="40">' \
                               f'<td width="7%">{index}</td>' \
                               f'<td width="9%">{record[2]}</td>' \
                               f'<td width="10%">{record[3]}</td>' \
                               f'<td width="20%">{record[4]}</td>' \
                               f'<td width="7%" bgcolor="{color}">{record[5]}</td>' \
                               f'<td width="15%">{str(record[6])}</td>' \
                               f'<td width="15%">{record[7]}</td>' \
                               f'<td width="10%">{screenshot}</td></tr>'
            content = content.replace('$test_records', test_record)
            report_path = os.path.join(Project.get_resource_path('report'),
                                       f'report_{self.version}.html')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)

    # 定义一个压缩测试报告的方法
    def compress_report(self):
        report_path = Project.get_resource_path('report')
        # 构建压缩文件的路径
        file = os.path.join(report_path, f'report_{self.version}.zip')
        # 构造压缩文件对象
        zip_file = zipfile.ZipFile(file, 'w', zipfile.ZIP_LZMA)
        filelist = []
        # 利用os模块的walk方法来遍历指定路径下的所有文件
        # 这里大家也可以不用这个方法，而是自己利用递归算法实现一个依据指定目录遍历所有文件的函数。
        for root, folders, filenames in os.walk(report_path):
            for folder in folders:
                filelist.append(os.path.join(root, folder))
            for filename in filenames:
                if self.version in filename and not filename.endswith('zip'):
                    filelist.append(os.path.join(root, filename))
        for file in filelist:
            # 注意write方法用来将文件压缩到zip_file对象中，
            # 第一个参数是文件路径，第二个参数叫做锚地址，这个参数用来控制压缩后文件的层级。
            zip_file.write(file, file.split('report', 1)[1])
        zip_file.close()
        return file

    # 定义一个发送邮件的方法
    def send_report(self, attachment):
        sender = 'student@woniuxy.com'
        receivers = ['tom@woniuxy.com', 'jerry@woniuxy.com']
        # 这是一封简单邮件的正文和标题的用法
        # message = MIMEText('这是一封来自python的邮件', 'text', 'utf-8')
        # message['Subject'] = Header('邮件标题', 'utf-8')
        # 带有附件的邮件构造方法
        # 构建一个可以添加邮件附件的对象
        message = MIMEMultipart()
        # MIMEText用于构建邮件正文，有三个参数：
        # 第一个参数是邮件内容
        # 第二个参数是邮件类型
        # 第三个参数是邮件的字符编码类型
        message.attach(MIMEText('<p style="color:red;font-size:30px">'
                                '四月一日你知道是什么日子吗？</p>', 'html', 'utf-8'))
        # 构建邮件标题，注意Subject拼写不能错
        # Header用于构建标题，有2个参数
        # 第一个参数是邮件标题
        # 第二个参数是标题字符的编码类型
        message['Subject'] = Header('节日快乐', 'utf-8')
        # 以二进制方式读取邮件附件
        with open(attachment, 'rb') as f:
            # 构建邮件附件对象
            attach = MIMEApplication(f.read())
        attach.add_header('Content-Disposition', 'attachment',
                          filename=os.path.basename(attachment))
        message.attach(attach)
        # 邮件发送处理
        try:
            # smtp_obj = smtplib.SMTP_SSL() # 针对邮箱发件设置勾选了SSL的情况使用
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect('smtp.woniuxy.com', 25)
            # 某些邮箱安全性高，默认设置不允许客户端通过密码登录邮箱，要求必须生成客户端访问密钥或者令牌，
            # 那此时密码处就需要输入这个单独生成的密钥或者令牌。
            # 当然你也可以通过修改降低邮箱的安全性设置，允许通过密码登录的方式解决。
            smtp_obj.login('student@woniuxy.com', '123456')
            smtp_obj.sendmail(sender, receivers, message.as_string())
            self.logger.info('邮件发送成功')
            smtp_obj.close()
        except smtplib.SMTPException as e:
            self.logger.info(f'邮件发送失败。失败原因：{str(e)}。')



if __name__ == '__main__':
    reporter = Reporter('0.0.2')
    # reporter.write_report('登录', 'UI测试', '输入正确的用户名和密码进行登录', '成功', '无', '无')
    # reporter.write_report('登录', 'UI测试', '输入错误的用户名和密码进行登录', '失败', '无', '无')
    # reporter.write_report('销售', 'UI测试', '输入正确的订单号', '错误', '无', '无')
    # reporter.write_report('销售', 'UI测试', '输入错误的订单号', '成功', '无', '无')
    # reporter.write_report('销售', 'UI测试', '输入正确的单价', '失败', '无', '无')
    # reporter.write_report('销售', 'UI测试', '输入错误的单价', '成功', '无', '无')
    # reporter.build_report()
    reporter.compress_report()
