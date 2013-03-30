#!/usr/bin/env python3
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
import sys
from jw2html import JW2HTML

if __name__ == '__main__':
    if len(sys.argv) > 1:
        issue_no = sys.argv[1]
    else:
        issue_no = None # current issue
    JW2HTML(issue_no).run()
