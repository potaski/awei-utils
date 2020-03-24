#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date: 2019-06-20
# @File: example.py
# @Author: zhangwei
# @Desc: graphviz示例


# 导入模块
import graphviz as gv

def pic_1():
    # Graph 一般性连线
    g = gv.Graph(format='svg')
    g.attr(size='6,6')
    g.node_attr.update(color='lightblue2', style='filled')
    g.node('')
    g.node('B')
    g.edge('A', 'B')
    # 生成PNG图片
    filename = g.render(filename='pic_1')
    print(filename)


def pic_2():
    # Digraph 一般性连线
    g = gv.Digraph(format='svg')
    g.attr(size='6,6')
    g.node_attr.update(color='lightblue2', style='filled', shape='box')
    g.edge('短信应用', 'ToB前台')
    g.edge('短信应用', '数据库')
    g.edge('ToB前台', 'ToB后台')

    # 生成PNG图片
    filename = g.render(filename='pic_2')
    print(g.pipe())


if __name__ == "__main__":
    # pic_1()
    pic_2()