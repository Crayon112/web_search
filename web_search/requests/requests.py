# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""网络请求

@File: requests.py
@Time: 2022/07/13 09:25:45
@Author: Crayon112
@SoftWare: VSCode
@Description: 网络请求

"""

from http.client import HTTPResponse
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode


def get(url: str, headers: dict, params: dict or str = None) -> HTTPResponse:
    if not isinstance(params, str) and params is not None:
        params = urlencode(params)
    if params:
        url += params if url.endswith('?') else ('?' + params)
    req = Request(url, headers=headers)
    resp = urlopen(req)
    return resp


def post(url: str, headers: dict, data: dict or bytes or str = None) -> HTTPResponse:
    if isinstance(data, str):
        data = data.encode()
    elif isinstance(data, bytes):
        data = data
    elif data is not None:
        data = json.dumps(data).encode("utf-8")

    req = Request(url, headers=headers, data=data)
    resp = urlopen(req)
    return resp
