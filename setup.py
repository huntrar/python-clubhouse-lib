#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import clubhouse_lib


def read(*names):
    values = dict()
    extensions = [".txt", ".rst"]
    for name in names:
        value = ""
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values


long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read(
    "README", "CHANGES"
)

setup(
    name="clubhouse-lib",
    version=clubhouse_lib.__version__,
    description="The unofficial Python client library for the Clubhouse API.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Bug Tracking",
    ],
    keywords="clubhouse clubhouse-lib clubhouse-api",
    author="Hunter H",
    author_email="huntrar@gmail.com",
    maintainer="Hunter H",
    maintainer_email="huntrar@gmail.com",
    url="https://github.com/huntrar/python-clubhouse-lib",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
)
