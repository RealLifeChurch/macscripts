#!/usr/bin/env python
import logging

module_logger = logging.getLogger("rlc_deploy.pullscripts")

#----------------------------------------------------------------------
def add(x, y):
    """"""
    logger = logging.getLogger("rlc_deploy.pullscripts.add")
    logger.info("added %s and %s to get %s" % (x, y, x+y))
    return x+y
