<b>python-installer.sh</b> - Detect OS type and installs appropriate python2.7 and python3.4 environment.

<b>oracle-ntp-dns.py</b> - Detects OS type, download and configures DNS and NTP servers.

The <b>jinja2temps/iplist</b> file contains IP configuration for DNS and NTP servers. If you intend to use different IPs please edit the file content to correspond to your environment. Please adhere the following rules while changing the configuration: each IP address must follow the sting starting from <b>#</b>.
<center>iplist file template:<br>
    # vmrac1.rac.lan<br>
<b>192.168.56.110</b><br>
    # vmrac2.rac.lan<br>
<b>192.168.56.111</b><br>
    # vmrac1-vip.rac.lan<br>
<b>192.168.56.112</b><br>
    # vmrac2-vip.rac.lan<br>
<b>192.168.56.113</b><br>
    # rac-scan.rac.lan<br>
<b>192.168.56.114<br>
192.168.56.115<br>
192.168.56.116</b></center>

The script asks to input an IP address of the DNS server (local or remote), user name and password of privileged user and domain name which will be used for Oracle Public Network.
