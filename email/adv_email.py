#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
-------------------- Copyright --------------------
Date    : 2018-12-11 08:20:31
Author  : zhangwei (potaski@qq.com)
Describe: email handler
Version : 1.0.0
-------------------- End --------------------
"""


from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def adv_mail_handler(sendto, title, content, files={}):
    """ send email with files
    :param sendto: reciver
    :param title: email title
    :param content: email content
    :param files: {file_name: file_content} file_content is bytes
    """
    smtp_serv = '192.168.1.1:25'
    sendfrom = "运维自动化<admin@autoops.com>"
    # parser email
    msg = MIMEMultipart()
    msg['From'] = sendfrom
    msg['To'] = sendto
    msg['Subject'] = Header(title, 'utf-8')
    msg.attach(MIMEText(content, _subtype='plain', _charset='UTF-8'))
    for filename, content in files.items():
        att = MIMEText(content, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
        msg.attach(att)
    # send email
    smtp = smtplib.SMTP()
    smtp.connect(smtp_serv)
    res = smtp.sendmail(sendfrom, sendto, msg.as_string())
    smtp.quit()
    if len(res) == 0:
        return True, res
    else:
        return False, res


if __name__ == '__main__':
