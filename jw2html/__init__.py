#!/usr/bin/env python3
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
__docformat__ = "epytext en"
import sys, logging

VERSION = '0.2'

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from .jw2html import JW2HTML
__all__ = ['VERSION', 'JW2HTML']


def main():
    print('.oOo. Welcome to JW2HTML version %s .oOo.' % VERSION)
    if len(sys.argv) > 1:
        issue_no = sys.argv[1]
    else:
        issue_no = None # current issue
    from .config import settings
    JW2HTML(settings, issue_no).run()
