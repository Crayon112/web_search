# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""Build 代码文件.

@File: setup.py
@Time: 2022/07/13 16:45:19
@Author: Crayon112
@SoftWare: VSCode
@Description: Build 代码文件.

"""

import os

import setuptools

with open("README.md", 'r', encoding="utf-8") as markdown_intro:
    long_description = markdown_intro.read()

with open(os.path.join("web_search", "__about__.py")) as rfile:
    v_dict = {}
    exec(rfile.read(), v_dict)
    version = v_dict['__version__']


setuptools.setup(
    name="feishu_sdk",
    version=version,
    author="Crayon112",
    description="web search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Crayon112/web_search",
    test_suite="nose.collector",
    tests_require=["nose"],
    packages=setuptools.find_packages(
        exclude=[
            "test", "search/SkyGrass", "ocr",
        ],
    ),
    package_dir={"web_search": "web_search"},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    project_urls={
        "Source": "https://github.com/Crayon112/web_search",
    },
)
