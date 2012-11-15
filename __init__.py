#!/usr/bin/env python
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
import sys
from jw2html import JW2HTML
from settings import USER, PASSWORD, SERVER, URI_INDEX, CACHEDIR

if __name__ == '__main__':
    if len(sys.argv) > 1:
        URI_INDEX = '/artikel/' + sys.argv[1] + '/'
    JW2HTML(USER, PASSWORD, SERVER, URI_INDEX, CACHEDIR).run()
