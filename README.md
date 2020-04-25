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

[nordvpn-server-find](https://github.com/mrzool/nordvpn-server-find): Pulled at first run if it does not exist in the working directory
## Installation


Configure the Software Dependencies listed above except for nordvpn-server-find, this will be done by the shell script

Pull down the repository:

    git clone https://github.com/nomodz4real/Pfsense-Vpn-Refresh.git

Navigate inside the folder created:

    cd Pfsense-Vpn-Refresh/

Create a file with your pfSense server's admin account password to be used by the script via sshpass:

    echo "youadminpassword" > .pfsensepassfile

Create a file with your pfSense server's ip address and listening port, be mindful to add a space between the two:

    echo "ipaddress port" > .pfsense_ip_and_port

Create a file with your pfSense-fauxAPI key and secret that you would have generated in the steps to installing the faux-api from https://github.com/ndejong/pfsense_fauxapi . Be mindful of keeping a space between the key and secret

    echo "pfsensekey pfsensesecret" > .pfsense_key_and_secret

(Optional)
To keep your password secret run the following commands to ensure that only root has access to the files and will require the script be run as root with sudo. Otherwise anyone in your group can access you password and keys.

 `sudo chmod 760 .pf*;sudo chown root:sudo vpnrefre.sh servermanipulation.py reachout_to_pfsense.py ./.pf*`

***Note*** When running `sudo chown root:sudo vpnrefre.sh servermanipulation.py reachout_to_pfsense.py ./.pf*` make sure that you add the correct sudo group you may have configured on your system, for example the sudo group could also be named "wheel"

To run:

./vpnrefre.sh 

or if you are using the secure method

sudo ./vpnrefre.sh 

You can also add this to your crontab or systemd timers as desired to run in the background
