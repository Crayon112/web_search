# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""工具函数.

@File: utils.py
@Time: 2022/07/13 09:20:03
@Author: Crayon112
@SoftWare: VSCode
@Description: 工具函数

"""
import json
from urllib.request import Request


def update_headers(req: Request, header: dict) -> Request:
    """更新某请求的请求头."""
    for k, v in header.items():
        req.add_header(k, v)
    return req


def parse_resp_data(resp_data: str or bytes) -> dict or str:
    """解析响应数据."""
    if isinstance(resp_data, bytes):
        resp_data = resp_data.decode()
    elif isinstance(resp_data, str):
        resp_data = resp_data
    else:
        raise NotImplementedError("无法处理返回数据")
    try:
        resp_data = json.loads(resp_data)
    except Exception:
        pass
    return resp_data
