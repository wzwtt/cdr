#!/usr/bin/env python
# -*- coding:utf-8 -*-
# cython : language_level=3
# @Time  : 2020-12-19, 0019 23:08
# @Author: 佚名
# @File  : excepthook.py

import sys
from requests import ReadTimeout
from requests.exceptions import ProxyError

from cdr.utils import Log
from cdr.config import LOG_DIR_PATH


def __my_except_hook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' % (exc_type.__name__, exc_value)

    Log.v("")
    Log.e(msg, is_show=False)
    if isinstance(exc_type, ReadTimeout)\
        or isinstance(exc_type, ConnectionError)\
        or isinstance(exc_type, ProxyError):
        Log.e("网路不稳定，请待网路恢复后重启程序，按回车键退出程序")
    else:
        Log.e("未知异常，请上报此错误（error-last.txt）给GM，按回车键退出程序")
        Log.e(f"你可以在“main{LOG_DIR_PATH[1:]}”下找到error-last.txt")
        Log.create_error_txt()
    input()
    sys.exit(1)


def hook_except():
    sys.excepthook = __my_except_hook
