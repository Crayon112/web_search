# !usr/bin/env python
# -*- encoding: utf-8 -*-

"""搜索类基类.

@File: search_api.py
@Time: 2022/07/12 22:03:37
@Author: Crayon112
@SoftWare: VSCode
@Description: 搜索类基类

"""

from ..user.user import User


class SearchAPI(object):
    """搜索基类."""

    def __init__(self, user: User, **kwargs) -> None:
        """初始化."""
        self.user = user
        self.kwargs = kwargs

    def search(self, keyword, **kwargs) -> bool:
        """精确匹配是否在数据库中."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__class__.__name__
