#!/usr/bin/env python
# coding:utf8

from werkzeug.utils import secure_filename
import random
import string


def get_ext(filename):
    try:
        ext = secure_filename(filename).split('.')[-1]
    except IndexError:
        ext = 'jpg'
    return ext


def random_name():
    return ''.join([random.choice(string.letters + string.digits) for i in range(14)])


def random_file_name(filename):
    return '%s.%s' % (random_name(), get_ext(filename))
