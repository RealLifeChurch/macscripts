#!/usr/bin/env python

from os import remove, close, path, rename, umask, symlink, unlink, walk, makedirs
import subprocess
import argparse
import logging
import logging.config
import sys
import plistlib
import optparse
import pull_scripts
import os
import urllib2


#Configure Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("rlc_deploy")

#Set some variables
deploy_dir = './'
config_plist = os.path.join(deploy_dir, 'test.plist')
script_dir = os.path.join(deploy_dir, 'scripts')
packages_dir = os.path.join(deploy_dir, 'packages')
installer = '/usr/sbin/installer'


#Configure Arguments
usage = "%prog [options]"
o = optparse.OptionParser(usage=usage)


o.add_option("--plist",
    help=("Optional. Path to an XML plist file containing "
          "key/value pairs for Version, Name, Output directory, Identifier, "
          "and Packages. "))

opts, args = o.parse_args()

def ip_addresses():
    command = "ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}' | wc -l"
    proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
    return proc.communicate()[0].replace('\n', '')

def all_done():
    if not os.listdir(packages_dir):
        sleep_time=10
        time.sleep(sleep_time)
        cleanup()
        subprocess.call(['/sbin/reboot'])



def main():
    #Don't run this yet.... enable in the end
    #subprocess.call(['/usr/sbin/networksetup', '-detectnewhardware'])
    # Check if the network is up
    success = False
    max_retries = 3
    retries = 0
    while retries < max_retries:
        print ip_addresses()
        if ip_addresses().strip() != "0":
            logger.info('Network connection is active. ')
            success = True
            break
        else:
            logger.info('No Connection Yet, trying again in 5 seconds')
            time.sleep(5)
            retries += 1

    if not success:
        logger.critical('No Connection Available')
        sys.exit()

    plist_opts = plistlib.readPlist(config_plist)
    # 'application' code
    #logger.debug('debug message')
    #logger.info('info message')
    #logger.warn('warn message')
    #logger.error('error message')
    #logger.critical('critical message')
    #result = pull_scripts.add(7, 8)

    # Check if we're using a plist.
    # If there aren't packages and no plist (with packages in), bail
    plist_opts = {}
    if opts.plist:
        try:
            plist_opts = plistlib.readPlist(opts.plist)
        except (ExpatError, IOError), err:
            fail('Could not read %s: %s' % (opts.plist, err))


    # Run over all of the packages and see if they look OK
    boot_scripts = plist_opts.get('Scripts')
    logger.info('Getting Scripts:')
    logger.info('----------------------------------------------------------------')
    for script in boot_scripts:
        logger.info ('%s' % script)
    logger.info('----------------------------------------------------------------')
    script_number = len(boot_scripts)
    logger.info("Number Of Scripts: %s" % script_number)

if __name__ == '__main__':
    main()
