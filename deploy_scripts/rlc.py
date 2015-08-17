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
import stat
import shutil

#Configure Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("rlc_deploy")

#Set some variables
deploy_dir = './deploy-scripts/'
script_dir = os.path.join(deploy_dir, 'scripts')
config_plist = os.path.join(deploy_dir, 'config.plist')
shutil.copy2('logging.conf', script_dir)
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

def Exec(cmd):
  """Executes a process and returns exit code, stdout, stderr.
  Args:
    cmd: str or sequence, command and optional arguments to execute.
  Returns:
    Tuple. (Integer return code, string standard out, string standard error).
  """
  if type(cmd) is str:
    shell = True
  else:
    shell = False
  try:
    p = subprocess.Popen(
      cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr
  except (IOError, OSError), e:
    return (99, '', str(e))

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0444) >> 2    # copy R bits to X
    os.chmod(path, mode)

def ip_addresses():
    command = "ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}' | wc -l"
    proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
    return proc.communicate()[0].replace('\n', '')

def all_done():
    if not os.listdir(script_dir):
        sleep_time=10
        time.sleep(sleep_time)
        cleanup()
        #subprocess.call(['/sbin/reboot'])

def cleanup():
    log_path = open(logfile, 'a')
    log.info('No more packages have been found to install, cleaning up.')
    # remove launchdaemon
    plist_opts = plistlib.readPlist(config_plist)
    launchd = os.path.join('/Library/LaunchDaemons/', plist_opts.get('LaunchDaemon'))
    os.remove(launchd)
    # remove launchagent
    os.remove('/Library/LaunchAgents/se.gu.it.LoginLog.plist')
    # remove loginlog.app
    shutil.rmtree('/Library/PrivilegedHelperTools/LoginLog.app')
    # remove firstboot_dir
    shutil.rmtree(deploy_dir)

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
    download_path = os.path.split(plist_url)
    download_path = download_path[0]
    print download_path
    logger.info('Downloading and Running:')
    logger.info('----------------------------------------------------------------')
    for script in boot_scripts:
        s = '/'
        scripts = download_path, script
        download = s.join(scripts)
        script_name = os.path.basename(script)
        logger.info ('Starting %s' % script_name )
        logger.info ('--------')
        #download_file.downloadChunks(download,script_dir)
        make_executable(script_dir + '/' + script_name)
        process = subprocess.Popen([script_dir + '/' + script_name])
        process.wait()
        logger.info('Finished %s' % script_name)
        logger.info('--------')
    logger.info('----------------------------------------------------------------')
    script_number = len(boot_scripts)
    logger.info("Number Of Scripts: %s" % script_number)
    #cleanup()

if __name__ == '__main__':
    main()
