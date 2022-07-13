# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""用户类.

@File: user.py
@Time: 2022/07/12 22:02:17
@Author: Crayon112
@SoftWare: VSCode
@Description: 用户类

"""


class User(object):
    """用户类."""

    def __init__(self, username, password, **kwargs) -> None:
        """用户初始化."""
        self.username = username
        self.password = password
        self.kwargs = kwargs
