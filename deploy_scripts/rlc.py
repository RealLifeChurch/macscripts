#!/usr/bin/env python

from os import remove, close, path, rename, umask, symlink, unlink, walk, makedirs
import subprocess
import argparse
import logging
import logging.config
import sys
import plistlib
import optparse
import download_file
import os


#Configure Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("rlc_deploy")

#Set some variables
deploy_dir = './deploy/'
script_dir = os.path.join(deploy_dir, 'scripts')
if not os.path.exists(script_dir):
    os.makedirs(script_dir)
#Configure Arguments
usage = "%prog [options]"
o = optparse.OptionParser(usage=usage)

o.add_option("-p", "--plist",dest="plist_url",
              help=("Optional. Path to an XML plist file containing "
                    "key/value pairs for Version, Name, Output directory, Identifier, "
                    "and Packages. "), metavar="PLIST_FILE")


opts, args = o.parse_args()
plist_name = os.path.basename(opts.plist_url)
config_plist = os.path.join(deploy_dir, plist_name)

plist_url = opts.plist_url
logger.info(plist_url)

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
    download_file.downloadChunks(opts.plist_url,deploy_dir)
    plist_opts = plistlib.readPlist(config_plist)
    # Check if we're using a plist.
    # If there aren't packages and no plist (with packages in), bail
    plist_opts = {}
    plist_opts = plistlib.readPlist(config_plist)


    # Run over all of the packages and see if they look OK
    boot_scripts = plist_opts.get('Scripts')
    logger.info('Getting Scripts:')
    logger.info('----------------------------------------------------------------')
    for script in boot_scripts:
        logger.info ('%s' % script)
    logger.info('----------------------------------------------------------------')
    script_number = len(boot_scripts)
    logger.info("Number Of Scripts: %s" % script_number)
    os.remove(config_plist)
    download_path = os.path.split(plist_url)
    print download_path[0]
if __name__ == '__main__':
    main()
