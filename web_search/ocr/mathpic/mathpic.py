# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""Mathpic OCR 识别类.

@File: mathpix.py
@Time: 2022/07/13 09:04:25
@Author: Crayon112
@SoftWare: VSCode
@Description: Mathpic OCR 识别类.

"""
import base64
import hashlib
import time
import uuid
from urllib.parse import urlencode

from web_search.requests.utils import parse_resp_data

from ...requests import post
from ..ocr import OCR


class MathpicOCR(OCR):
    """有道OCR接口类实现."""

    text_service = 'https://openapi.youdao.com/ocrapi'

    def __init__(self, app_key, app_secret):
        """初始化."""
        self.app_key = app_key
        self.app_secret = app_secret

        self.headers = {
            'app_id': self.app_key,
            'app_key': self.app_secret,
            'Content-type': 'application/x-www-form-urlencoded',
        }

    def _encrypt(self, src: str, salt: str, curtime: str) -> str:

        def _truncate(s: str) -> str:
            if len(s) <= 20:
                return s
            return s[:10] + str(len(s)) + s[-10:]

        encrypt_str = self.app_key + _truncate(src) + salt + \
            curtime + self.app_secret

        _hash = hashlib.sha256()
        _hash.update(encrypt_str.encode('utf-8'))
        return _hash.hexdigest()

    def ocr(self, pic_bin=None, url=None, **kwargs) -> str:
        """OCR识别.

        Args:
            pic_bin (bytes, optional): 要识别的图片二进制
            url (str, optional): 待识别的图片url

        Returns:
            str, 识别出的文本
        """
        if not (pic_bin or url):
            raise ValueError("pic_bin或url必须被提供")

        src = self._image_uri(pic_bin) if pic_bin else url

        def _ocr(src):
            salt = str(uuid.uuid1())
            curtime = str(int(time.time()))

            args = {
                "img": src,
                "langType": "en",
                "detectType": "10012",
                "imageType": "1",
                "appKey": self.app_key,
                "salt": salt,
                "sign": self._encrypt(src, salt, curtime),
                "docType": "json",
                "signType": "v3",
                "curtime": curtime,
            }

            r = post(
                self.text_service,
                data=urlencode(args),
                headers=self.headers,
            )

            try:
                data = r.read()
                output = parse_resp_data(data)
                if output.get("errorCode") != '0':
                    raise ValueError
            except Exception as e:
                raise e

            if "Result" in output:
                text_list = []
                for region in output["Result"]["regions"]:
                    row_texts = []
                    for row in region["lines"]:
                        row_texts.append(row["text"])
                    text_list.extend(row_texts)
                return text_list
            else:
                return []

        res = _ocr(src)
        return "".join(res)

    def _image_uri(self, img_bin):
        return "data:image/wmf;base64," + base64.b64encode(img_bin).decode()
