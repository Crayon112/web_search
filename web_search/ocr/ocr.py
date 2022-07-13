# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
OCR识别基类

@File: ocr.py
@Time: 2022/07/13 09:13:42
@Author: Crayon112
@SoftWare: VSCode
@Description: OCR识别基类

"""


class OCR(object):
    """OCR基类"""

    def ocr(self, **kwargs) -> str:
        """
        ocr接口方法

        Returns:
            {str}: 识别结果
        """
        raise NotImplementedError
