#!/usr/bin/env python
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
from jw2html import JW2HTML
from settings import USER, PASSWORD, SERVER, URI_INDEX, CACHEDIR

if __name__ == '__main__':
    JW2HTML(USER, PASSWORD, SERVER, URI_INDEX, CACHEDIR).run()
