#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# 좌표구하기
class Point:
        def __init__(self, x, y):
                self.x = x
                self.y = y
        def setx(self, x):
                self.x = x
        def sety(self, y):
                self.y = y
        def get(self):
                return (self.x, self.y)
        def move(self, dx, dy):
                self.x += dx
                self.y += dy
        