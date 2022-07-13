# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""幽灵鲨接口实现

@File: phantom_shark.py
@Time: 2022/07/12 22:09:24
@Author: Crayon112
@SoftWare: VSCode
@Description: 幽灵鲨接口实现

"""

from ...globals import HEADERS
from ...requests import get, parse_resp_data, post
from ...user import User
from ..search_api import SearchAPI


class PhantomShark(SearchAPI):

    _login_api = "http://47.99.236.231/api/login"

    _search_api = "http://47.99.236.231/api/client/checkClient"

    _headers = HEADERS

    def __init__(self, user: User, **kwargs) -> None:
        super().__init__(user, **kwargs)
        self._is_login, data = self._login()
        if self._is_login:
            self._token = self._get_token_from_data(data)
            self.add_auth_headers()

    def _get_token_from_data(self, data):
        try:
            return data["data"]["token"]
        except Exception:
            return ''

    def add_auth_headers(self):
        self._headers.update({
            "Authorization": f"Bearer {self._token}",
        })

    def _login(self):
        resp = post(
            self._login_api, data={
                "code": "",
                "pwd": self.user.password,
                "tenent_id": "1",
                "username": self.user.username,
            }, headers=self._headers,
        )
        try:
            data = resp.read()
            return int(resp.status) == 200, parse_resp_data(data)
        except Exception:
            return False, {}

    def search(self, keyword: str, **kwargs):
        resp = get(self._search_api, params={"keyword": keyword}, headers=self._headers)
        try:
            data = resp.read()
            data = parse_resp_data(data)["data"]["data"]
            res = [d["name"] for d in data]
        except Exception:
            res = set()
        return bool(res)
