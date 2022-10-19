
from pathlib import Path
import logging
import os

a='张三'
b='去逛街'
lista=['李四','赵云']

fa=a.format()
print('这是一个测试{0[0]}喜欢{0[1]}'.format(lista))

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
# '/home/cn/桌面/django/myblog_house/myblog '
