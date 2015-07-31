# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Utiltiy for measuring elapsed time
#
# From: http://www.huyng.com/posts/python-performance-analysis/
#
# Use like:
#   with Timer() as t:
#       pass

import time

class Timer(object):
    def __init__(self, name="", verbose=False):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end   = time.time()
        self.secs  = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'Timer[%s] %f ms' % (self.name, self.msecs)