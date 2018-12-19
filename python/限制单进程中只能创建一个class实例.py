#!/usr/bin/env python

import threading

class A:
    __instance = None
    __inited = None

    def __new__(cls):
        if not cls.__instance:
            A.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def print(self, tag):
        return tag


def a(arg):
    obj = A()
    print(id(obj), obj, obj.print(arg))


if __name__ == "__main__":
    for i in range(3):
        t = threading.Thread(target=a, args=(i,)).start()
    a('test')
    print('done')