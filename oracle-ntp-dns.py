#!/usr/bin/env python2.7

import sys
import os
import jinja2
from termcolor import colored, cprint
from fabric.api import *
from fabric.tasks import execute
import getpass

codepath = os.path.dirname(__file__)
outputdir = codepath+'/output/'
jinjadir = codepath+'/jinja2temps/'
iplist = jinjadir+'iplist'

iplistfile = colored(iplist, 'red', attrs=['reverse', 'blink'])
ntp = colored('NTP', 'green', attrs=['bold', 'underline'])
dns = colored('DNS', 'green', attrs=['bold', 'underline'])
ipadressess = colored('IP addresses', 'cyan', attrs=['bold'])
username = colored('username', 'green', attrs=['bold'])
password = colored('password', 'green', attrs=['bold'])
domainname = colored('domain name', 'green', attrs=['bold'])
dnsserverip= colored('DNS server IP', 'green', attrs=['bold'])
successfully = colored('successfully', 'green', attrs=['bold', 'underline'])

print('Script will install and configure '+ntp+' and '+dns+' ...')
print('It needs '+ipadressess+' for RAC dns records. Please edit '+iplistfile+' file for your design ...')
env.host_string = raw_input('Please enter '+dnsserverip+' address: ')
env.user = raw_input('Please enter '+username+' for UNIX/Linux server: ')
env.password = getpass.getpass('Please enter '+password+' for UNIX/Linux server: ')
domain = raw_input('Please enter '+domainname+' for RAC public network: ')

f=open(iplist, 'r')
lines=f.readlines()
racnode1 = lines[1].strip()
racnode2 = lines[3].strip()
rac1vip1 = lines[5].strip()
rac2vip2 = lines[7].strip()
rac_scan1 = lines[9].strip()
rac_scan2 = lines[10].strip()
rac_scan3 = lines[11].strip()
f.close()

templateLoader = jinja2.FileSystemLoader( searchpath=jinjadir )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPZFILE = 'zone.conf'
TEMPNTPFILE = 'ntp.conf'
TEMPDOMFILE = 'records.conf'
tempz = templateEnv.get_template( TEMPZFILE )
tempntp = templateEnv.get_template( TEMPNTPFILE )
tempdom = templateEnv.get_template( TEMPDOMFILE )

tempaVars = { "ns1" : env.host_string, 
        "domain" : domain, 
        "racnode1" : racnode1, 
        "racnode2" : racnode2, 
        "rac1vip1" : rac1vip1, 
        "rac2vip2" : rac2vip2, 
        "rac_scan1" : rac_scan1, 
        "rac_scan2" : rac_scan2, 
        "rac_scan3" : rac_scan3, }

outputzText = tempz.render( tempaVars )
outputrecText = tempdom.render( tempaVars )
outputntpText = tempntp.render( tempaVars )

with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    osver = run('uname -s')
    lintype = run('cat /etc/centos-release | awk \'{ print $1 }\'')

    if osver == 'Linux' and lintype == 'CentOS':
        getlbindpack = run('which named')
        bindlpidfile = run('cat /var/run/named/named.pid')
        bindlpid = run('ps waux|grep named | grep -v grep | awk \'{ print $2 }\'')
        getntppack = run('which ntpd')
        ntppid = run('ps waux | grep ntpd | grep -v grep | awk \'{ print $2 }\'')
        ntppidfile = run('cat /sys/fs/cgroup/systemd/system.slice/ntpd.service/tasks')

        if getlbindpack == '/usr/sbin/named' and bindlpidfile == bindlpid:
            print(' You have already installed and running bind ...')
            sys.exit()

        elif getlbindpack != '/usr/sbin/named':
            print(' Please be patient. DNS server will be installed and configured ...')
            run('yum -y install bind bind-utils bind-chroot')
            run('systemctl start named ; systemctl enable named')
            run('mkdir -p /var/log/bind/ /etc/namedb/{master,slave}')
            run('touch /var/log/bind/named.log /var/log/bind/query.log')
            run('chown -R named:named /var/log/bind/ /etc/namedb/{master,slave}')
            local('cp '+jinjadir+'named.conf '+outputdir)

            with open(outputdir+'zone_'+env.host_string+'.conf', 'wb') as dnszone:
                dnszone.write(outputzText)

            local('cat '+outputdir+'zone_'+env.host_string+'.conf >> '+outputdir+'named.conf')
            put(outputdir+'named.conf', '/etc/named.conf')

            with open(outputdir+domain+'.zone', 'wb') as records:
                records.write(outputrecText)

            put(outputdir+domain+'.zone', '/etc/namedb/master/')
            run('systemctl restart named')
            print('DNS server '+successfully+' installed and configured')

        if getntppack == '/usr/sbin/ntpd' and ntppid == ntppidfile:
            print(' You have already installed and running NTP ...')
            sys.exit()

        elif getntppack != '/usr/sbin/ntpd':
            print(' Please be patient. NTP server will be installed and configured ...')
            run('yum -y install ntp.x86_64')

            with open(outputdir+'ntp.conf', 'wb') as ntpfile:
                ntpfile.write(outputntpText)

            put(outputdir+'ntp.conf', '/etc/')
            run('systemctl start ntpd ; systemctl enable ntpd')
            print('NTP server '+successfully+' installed and configured')
