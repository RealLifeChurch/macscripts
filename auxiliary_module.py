#!/usr/bin/env python
import logging
import os
import sys

# create logger
module_logger = logging.getLogger('deployment.auxiliary')

class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger('deployment.auxiliary.Auxiliary')
        self.logger.info('creating an instance of Auxiliary')
    def do_something(self):
        self.logger.info('doing something')
        a = 1 + 1
        self.logger.info('done doing something')
        os.remove("auxiliary_module.py")
        os.remove("auxiliary_module.pyc")

def some_function():
    module_logger.info('received a call to "some_function"')
