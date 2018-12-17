#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
-------------------- Copyright --------------------
Date    : 2018-12-14 09:35:11
Author  : zhangwei (potaski@qq.com)
Describe: xlsx writer
Version : 1.0.0
-------------------- End --------------------
"""


import xlsxwriter
import uuid
import os


def parser_xlsx_data(input=[]):
    """ 生成xlsx数据
    input = [
        ['col_1', 'col_2', 'col_3'],  # row1
        ['col_1', 'col_2', 'col_3'],  # row2
    ]
    output = open(xlsx, 'rb').read()
    """
    xlsx = '{}-{}.xlsx'.format(uuid.uuid4(), uuid.uuid4())
    workbook = xlsxwriter.Workbook(xlsx)
    worksheet = workbook.add_worksheet()
    row = 0
    for line in input:
        col = 0
        for item in line:
            worksheet.write(row, col, item)
            col += 1
        row += 1
    workbook.close()
    output = open(xlsx, 'rb').read()
    os.remove(xlsx)
    return output


if __name__ == '__main__':
    ret = parser_xlsx_data(input=[['1', '2', '3'], ['4', '5', '6', '7']])
    # print(ret)
    with open('test.xlsx', 'wb') as f:
        f.write(ret)