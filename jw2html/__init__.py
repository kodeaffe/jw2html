#!/usr/bin/env python3
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
__docformat__ = "epytext en"
import sys

VERSION = '0.1'
from .jw2html import JW2HTML
__all__ = ['VERSION', 'JW2HTML']


def main():
    if len(sys.argv) > 1:
        issue_no = sys.argv[1]
    else:
        issue_no = None # current issue
    JW2HTML(issue_no).run()
