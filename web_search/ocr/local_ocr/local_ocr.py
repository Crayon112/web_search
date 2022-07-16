# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""本地OCR识别.

@File: __init__.py
@Time: 2022/07/16 18:53:30
@Author: Crayon112
@SoftWare: VSCode
@Description: 本地OCR识别

"""



from ..ocr import OCR
from ddddocr import DdddOcr


class LocalOCR(OCR):

    def ocr(self, pic_bin=None, **kwargs) -> str:
        """OCR识别.

        Args:
            pic_bin (bytes, optional): 要识别的图片二进制

        Returns:
            str, 识别出的文本
        """
        if not pic_bin:
            raise ValueError("pic_bin或url必须被提供")

        return DdddOcr(show_ad=False).classification(pic_bin)
