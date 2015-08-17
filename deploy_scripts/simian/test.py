#!/usr/bin/env python

import urllib2
from tempfile import mkstemp
from shutil import move, rmtree
from os import remove, close, path, rename, umask, symlink, unlink, walk, makedirs
import subprocess
import math
import time
import argparse
import re

parser = argparse.ArgumentParser(description='Installs and configures Puppet on OS X')
parser.add_argument('--server', help='The URL of the Puppet Server. Defaults to puppet.grahamgilbert.dev')
args = vars(parser.parse_args())

if args['server']:
    puppetserver = args['server']
else:
    puppetserver = 'puppet.reallifechurch.org'
def downloadChunks(url):
    """Helper to download large files
        the only arg is a url
       this file will go to a temp directory
       the file will also be downloaded
       in chunks and print out how much remains
    """

    baseFile = path.basename(url)

    #move the file to a more uniq path
    umask(0002)

    try:
        temp_path='/tmp'
        file = path.join(temp_path,baseFile)

        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                print math.floor( (downloaded / total_size) * 100 )
                if not chunk: break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:",e.code , url
        return False
    except urllib2.URLError, e:
        print "URL Error:",e.reason , url
        return False

    return file

def forget_pkg(pkgid):
    cmd = ['/usr/sbin/pkgutil', '--forget', pkgid]
    proc = subprocess.Popen(cmd, bufsize=1,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (output, unused_err) = proc.communicate()
    return output

def internet_on():
    try:
        response=urllib2.urlopen(puppetserver,timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def chown_r(path):
    makedirs(path)
    the_command = "chown -R root:wheel "+path
    serial = subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
    the_command = "chmod -R 777 "+path
    serial = subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]

if internet_on:

    the_command = "ioreg -c \"IOPlatformExpertDevice\" | awk -F '\"' '/IOPlatformSerialNumber/ {print $4}'"
    serial = subprocess.Popen(the_command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
    serial = re.sub(r'\s', '', serial)
    # remove the silly characters that VMware likes to put in occasionally
    serial = serial.replace("+", "")
    serial = serial.replace("/", "")
    certname = serial.lower()

    print "Server: %s" % puppetserver
    print "Certname: %s" % certname
