python-installer.sh - Detect OS type and installs appropriate python2.7 and python3.4 environment.

oracle-ntp-dns.py - Detects OS type, download and configures DNS and NTP servers.

The jinja2temps/iplist file contains IP configuration for DNS and NTP servers. If you intend to use different IPs please edit the file content to correspond to your environment. Please adhere the following rules while changing the configuration: each IP address must follow the sting starting from #.
iplist file template:
    # racnode1_host
    192.168.56.10
    # racnode2_host
    192.168.56.11
    # racnode1_VIP1
    192.168.56.12
    # racnode2_VIP2
    192.168.56.13
    # RAC_SCAN
    192.168.56.14
    192.168.56.15
    192.168.56.16

The script asks to input an IP address of the DNS server (local or remote), user name and password of privileged user and domain name which will be used for Oracle Public Network.
