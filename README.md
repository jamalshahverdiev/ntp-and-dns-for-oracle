<b>python-installer.sh</b> - Detect OS type and installs appropriate python2.7 and python3.4 environment.

<b>oracle-ntp-dns.py</b> - Detects OS type, download and configures DNS and NTP servers.

The <b>jinja2temps/iplist</b> file contains IP configuration for DNS and NTP servers. If you intend to use different IPs please edit the file content to correspond to your environment. Please adhere the following rules while changing the configuration: each IP address must follow the sting starting from <b>#</b>.
<center>iplist file template:
    # racnode1_host
    <b>192.168.56.10</b>
    # racnode2_host
    <b>192.168.56.11</b>
    # racnode1_VIP1
    <b>192.168.56.12</b>
    # racnode2_VIP2
    <b>192.168.56.13</b>
    # RAC_SCAN
    <b>192.168.56.14<br>
    192.168.56.15<br>
    192.168.56.16</b></center>

The script asks to input an IP address of the DNS server (local or remote), user name and password of privileged user and domain name which will be used for Oracle Public Network.
