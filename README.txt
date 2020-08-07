# Pfsense-Vpn-Refresh
A set of code to update the vpn client address in pfsense

### Confirmed working on:
Arch Linux

Should theoretically work on other versions of linux as long as the dependencies are met

### Software Dependencies:

pfSense v2.x

FauxAPI on pfsense - https://github.com/ndejong/pfsense_fauxapi configured and running

Python 3.X

Pip for python 3

pfsense-fauxapi python library:

    pip3 install pfsense-fauxapi
    
requests python library:

    pip3 install requests

## Installation

Configure the software dependencies listed above

Pull down the repository:

    git clone https://github.com/nomodz4real/Pfsense-Vpn-Refresh.git

Navigate inside the folder created:

    cd Pfsense-Vpn-Refresh/

To run:

`./tasks.py`

or if you are using the secure method

`sudo ./tasks.py`

Upon first run a file with your pfSense server's IP address and listening port will be created with sample data that would be needed, replace the values with your server's IP address and listening port, the Faux API can handle hostnames and https as well so you are not limited to using your pfsense server's IP address only

A file containing sample date for the fauxapi key and secret is also built upon first run, replace the values with your fauxapi's installs key and secret

These files are named:

`.pfsense_ip_and_port`
`.pfsense_key_and_secret`

and these files will be located in either /root/.vpnrefresh or /home/$USER/.vpnrefresh depending on whether you ran the script with sudo or not

(Secure Method)
To keep your fauxapi data secret run the following commands to ensure that only root has access to the files and will require the script be run as root with sudo. You will need to do this in the .vpnrefresh directory that is made upon first run. Otherwise anyone in your group can access your keys and secrets.

 `sudo chmod 760 .pf*;sudo chown root:sudo *.py .pf*`

***Note*** When running `sudo chown root:sudo *.py .pf*` make sure that you add the correct sudo group you may have configured on your system, for example the sudo group could also be named "wheel"

You can also add this to your crontab or systemd timers as desired to run in the background. Be sure to follow the best practices for your system on running python scripts from cron or systemd