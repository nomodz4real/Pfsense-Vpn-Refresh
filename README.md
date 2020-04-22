# Pfsense-Vpn-Refresh
A set of code to update the vpn client address in pfsense

### Confirmed working on:
Arch Linux

Should theoretically work on other versions of linux as long as the dependencies are met

### Software Dependencies:

pfSense v2.x

[FauxAPI on pfsense](https://github.com/ndejong/pfsense_fauxapi) 

Python 3.X

pfsense-fauxapi python library:

    pip3 install pfsense-fauxapi

jq

    sudo pacman -Sy jq
sshpass 

    sudo pacman -Sy sshpass

[nordvpn-server-find](https://github.com/mrzool/nordvpn-server-find):

    git clone https://github.com/mrzool/nordvpn-server-find.git
## Installation

Configure the Software Dependencies listed above except for nordvpn-server-find, we will do this later

Pull down the repository:

    git clone https://github.com/nomodz4real/Pfsense-Vpn-Refresh.git

Navigate inside the folder created:

    cd Pfsense-Vpn-Refresh/

Create a file with your pfSense server's admin account password to be used by the script via sshpass:

    echo "youadminpassword" > .pfsensepassfile

Create a file with your pfSense server's ip address and listening port, be mindful to add a space between the two:

    echo "ipaddress port" > .pfsense_ip_and_port

Pull down nordvpn-server-find repository inside the Pfsense-Vpn-Refresh folder:

    git clone https://github.com/mrzool/nordvpn-server-find.git

(Optional)
To keep your password secret run the following commands to ensure that only root has access to the files and will require the script be run as root with sudo

    chmod 755 *;chmod 744 .*;chown root:root * .*

To run:

    ./vpnrefre.sh 

or if you are using the secure method

    sudo ./vpnrefre.sh

 

You can also add this to your crontab or systemd timers as desired to run in the background
