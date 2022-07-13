# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""用户类

@File: user.py
@Time: 2022/07/12 22:02:17
@Author: Crayon112
@SoftWare: VSCode
@Description: 用户类

"""


class User(object):

    def __init__(self, username, password, **kwargs) -> None:
        self.username = username
        self.password = password
        self.kwargs = kwargs
