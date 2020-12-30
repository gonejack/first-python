#! /usr/bin/env python3

# coding=utf-8

# import numpy as np
#
# def softmax(ctrs):
#     tmp = np.max(ctrs)  # 得到最大值
#     ctrs -= tmp  # 利用最大值缩放数据
#     ctrs = np.exp(ctrs)  # 对所有元素求指数
#     tmp = np.sum(ctrs)  # 求元素和
#     ctrs /= tmp  # 求somftmax
#     return ctrs
#
# print softmax([1, 2, 3])
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int = 1

    def qq(self, i: int, s: str):
        print(self.x, self.y, i, s)


def abc():
    point = Point(1, 2)
    print("p is %s" % point)
    point.qq(1, "2")

    qq = "abc"
    qq.endswith("abc")


if __name__ == '__main__':
    quit(1)
