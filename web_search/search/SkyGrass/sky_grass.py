# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""天禾接口实现.

@File: sky_grass.py
@Time: 2022/07/12 22:42:59
@Author: Crayon112
@SoftWare: VSCode
@Description: 天禾接口实现.

"""

import datetime
import json
import os
from http.client import HTTPResponse
from urllib.parse import urlencode

from ...globals import HEADERS
from ...requests import get, parse_resp_data, post
from ...user.user import User
from ..search_api import SearchAPI

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class SkyGrass(SearchAPI):
    """天禾接口类实现."""

    _page_size = 10

    _login_api = "http://jmb1.tianheyunshang.com/admin/index/login.html"

    _search_api = \
        "http://jmb1.tianheyunshang.com/admin/basesetting/weixinoperate/index"

    _captcha_api = "http://jmb1.tianheyunshang.com/index.php?s=/captcha"

    _referer_url = \
        "http://jmb1.tianheyunshang.com/admin/basesetting/weixinoperate"

    _cached_headers = {}

    def __init__(self, user: User, **kwargs) -> None:
        """初始化过程."""
        super().__init__(user, **kwargs)
        self._headers = HEADERS
        self.retry = 10
        self.ocr = kwargs.get('ocr', None)

    def _add_extra_headers(self):
        extra_headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": self._referer_url,
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        self._headers = self._headers | extra_headers

    def _add_cookie(self, resp: HTTPResponse) -> None:
        cookie = resp.headers.get("Set-Cookie")
        self._headers.setdefault("Cookie", cookie)

    @property
    def _is_login(self):
        if self._cached_headers:
            self._headers = self._cached_headers
            return True
        is_login = False
        while not is_login and self.retry >= 0:
            resp = get(self._captcha_api, headers=self._headers)
            self._add_cookie(resp)
            try:
                img_bin = resp.read()
            except AttributeError:
                img_bin = b''
            captcha = self.ocr.ocr(pic_bin=img_bin)
            resp = post(
                self._login_api, headers=self._headers,  data=urlencode({
                    'username': self.user.username,
                    'password': self.user.password,
                    'captcha': captcha,
                }),
            )
            data = resp.read()
            resp_data = parse_resp_data(data)
            is_login = '成功' in resp_data
            self.retry -= 1
        return is_login

    def search(self, keyword, **kwargs) -> bool:
        """搜索接口方法实现."""
        if not self._is_login:
            return False
        else:
            self._cached_headers = self._headers
        self._add_extra_headers()
        data = {
            'sort': "weixin_id",
            "order": "desc",
            "offset": "0",
            "limit": str(self._page_size),
            "filter": f'{{"weixin_number":"{keyword}"}}',
            "op": '{"weixin_numer":"="}',
            "_": f'{int(datetime.datetime.now().timestamp())}',
        }
        resp = get(
            self._search_api,
            params=urlencode(data),
            headers=self._headers,
        )
        data: str = parse_resp_data(resp.fp)
        data = self._process_data(data)
        try:
            return int(data["total"]) != 0
        except Exception:
            return False

    def _process_data(self, data: str) -> dict:
        try:
            start, end = data.index('{'), data.index('}')
            return json.loads(data[start: end + 1])
        except Exception:
            return {}
