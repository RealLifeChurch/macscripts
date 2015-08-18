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
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
sys.stdout = Logger()

#Set some variables
deploy_dir = './deploy-scripts/'
script_dir = os.path.join(deploy_dir, 'scripts')
config_plist = os.path.join(deploy_dir, 'config.plist')
if not os.path.exists(script_dir):
    os.makedirs(script_dir)

shutil.copy2('logging.conf', script_dir)
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
print(plist_url)

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
    # remove launchdaemon
    launchd = os.path.join('/Library/LaunchDaemons/org.reallifechurch.deploy.plist')
    os.remove(launchd)
    # remove launchagent
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
            print('Network connection is active. ')
            success = True
            break
        else:
            print('No Connection Yet, trying again in 5 seconds')
            time.sleep(5)
            retries += 1

    if not success:
        print('No Connection Available')
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
    print('Downloading and Running:')
    print('----------------------------------------------------------------')
    for script in boot_scripts:
        s = '/'
        scripts = download_path, script
        download = s.join(scripts)
        script_name = os.path.basename(script)
        print ('Starting %s' % script_name )
        print ('--------')
        download_file.downloadChunks(download,script_dir)
        make_executable(script_dir + '/' + script_name)
        process = subprocess.Popen([script_dir + '/' + script_name])
        process.wait()
        print('Finished %s' % script_name)
        print('--------')
    print('----------------------------------------------------------------')
    script_number = len(boot_scripts)
    print("Number Of Scripts: %s" % script_number)
    #cleanup()

if __name__ == '__main__':
    main()
