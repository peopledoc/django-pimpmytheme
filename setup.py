#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
import sys

PY2 = sys.version_info[0] == 2
ROOT = dirname(abspath(__file__))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA


def read_relative_file(filename):
    """
    Returns contents of the given file, whose path is supposed relative
    to this module.

    """
    with open(join(ROOT, filename)) as f:
        return f.read()


NAME = 'django-pimpmytheme'
DESCRIPTION = ("Customise theme (css and template) on a per user/client "
               "whatever basis")
REQUIREMENTS = [
    'Django>=1.11,<2.0' if PY2 else 'Django>=1.11',
    'django-compressor>=2.2',
    'gitpython>1.0.0',
]
__VERSION__ = read_relative_file('VERSION').strip()


params = dict(
    name=NAME,
    description=DESCRIPTION,
    packages=['pimpmytheme'],
    version=__VERSION__,
    long_description=read_relative_file('README.rst'),
    author='Yohann Gabory',
    author_email='peopledoc@people-doc.com',
    url='https://github.com/peopledoc/django-pimpmytheme',
    license='MIT License',
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ],
)

if __name__ == '__main__':
    setup(**params)
