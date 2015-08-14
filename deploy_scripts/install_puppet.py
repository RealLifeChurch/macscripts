#!/usr/bin/env python

import logging
import auxiliary_module
import urllib2
import argparse

parser = argparse.ArgumentParser(description='Installs and configures OS X for Real Life Church ')
parser.add_argument('--server', help='The URL of the Puppet Server. Defaults to puppet.grahamgilbert.dev')
args = vars(parser.parse_args())

if args['server']:
    puppetserver = args['server']
else:
    puppetserver = 'google.com'

def internet_on():
    try:
        response=urllib2.urlopen(puppetserver,timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

if internet_on:

    # create logger with 'spam_application'
    logger = logging.getLogger('deployment')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('deployment.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('creating an instance of auxiliary_module.Auxiliary')
    a = auxiliary_module.Auxiliary()
    logger.info('created an instance of auxiliary_module.Auxiliary')
    logger.info('calling auxiliary_module.Auxiliary.do_something')
    a.do_something()
    logger.info('finished auxiliary_module.Auxiliary.do_something')
    logger.info('calling auxiliary_module.some_function()')
    auxiliary_module.some_function()
    logger.info('done with auxiliary_module.some_function()')
