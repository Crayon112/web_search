# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""六台阶接口实现.

@File: six_soft.py
@Time: 2022/07/12 22:21:34
@Author: Crayon112
@SoftWare: VSCode
@Description: 六台阶接口实现

"""
from http.client import HTTPResponse
from urllib.parse import quote, urlencode

from ...globals import HEADERS
from ...requests import parse_resp_data, post
from ...user import User
from ..search_api import SearchAPI


class SixSoft(SearchAPI):
    """六台阶接口实现."""

    _page_size = 20

    _login_api = \
        "https://crm07.hrtl.com.cn/CRM3_211022145705_283945/AJAX/Login.ashx"

    _referer_url = \
        "https://crm07.hrtl.com.cn/CRM3_211022145705_283945/Login.aspx"

    _search_api = \
        "https://crm07.hrtl.com.cn/CRM3_211022145705_283945/AJAX/GetList.ashx"

    def __init__(self, user: User, **kwargs) -> None:
        """初始化.

        Args:
            user {User}: 用户类

        """
        super().__init__(user, **kwargs)
        self._headers = HEADERS

    def _add_referer_header(self):
        self._headers.update({'referer': self._referer_url})

    def _add_cookie(self, resp: HTTPResponse):
        cookie = resp.headers.get("Set-Cookie")
        self._headers.setdefault("Cookie", cookie)

    @property
    def _is_login(self) -> bool:
        """登陆状态."""
        self._add_referer_header()
        resp = post(
            self._login_api,
            data=urlencode({
                "UserName": quote(self.user.username),
                "Password": quote(self.user.password),
            }),
            headers=self._headers,
        )
        self._add_cookie(resp)
        return int(resp.status) == 200

    def search(self, keyword, **kwargs):
        """搜索接口实现."""
        if not self._is_login:
            return False
        resp = post(
            self._search_api, data=urlencode({
                'Cate': 'Get_List',
                'FormName': 'Client_Contact',
                'Search':
                    f'Search_KeyWord$:${keyword}$,'
                    '$Search_KeyWord_Cate$:$Blur$,'
                    '$Search_KeyWord_ColName$:$Name',
                'PageIndex': '1',
                'PageSize': str(self._page_size),
            }), headers=self._headers,
        )
        data = resp.read()
        data = parse_resp_data(data)
        return bool(data["Data"])
