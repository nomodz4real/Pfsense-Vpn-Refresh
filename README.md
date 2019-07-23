# Pfsense-Vpn-Refresh
A set of code to update the vpn client address in pfsense

Server OS: Arch Linux

Software Dependencies: FauxAPI on pfsense - unofficial api developed by ndejong (https://github.com/ndejong/pfsense_fauxapi) as root on pfsense: fetch https://raw.githubusercontent.com/ndejong/pfsense_fauxapi_packages/master/pfSense-pkg-FauxAPI-1.3_4.txz

and

pkg-static install pfSense-pkg-FauxAPI-1.3_4.txz

Python 3.7 (sudo pacman -S python) Pip (sudo pacman -S python-pip) pfsense-fauxapi python library (sudo pip3 install pfsense-fauxapi) jq (sudo pacman -S jq) nordvpn-server-find (sudo git clone https://github.com/mrzool/nordvpn-server-find.git)

Application and sub applications: /scriptsubdirectory/vpnrefre.sh Main app /scriptsubdirectory/vpnrefreshsubscripts/getconfig.py App to pull config /scriptsubdirectory/vpnrefreshsubscripts/setconfig.py App to apply config /scriptsubdirectory/vpnrefreshsubscripts/servermanipulation.py App to modify pulled config

Creates: bestserverfound - text file with vpn servername found by nordvpn-server-find client.json - config file pulled by getconfig.py autooutput.json - config file made by servermanipulation.py and used by setconfig.py to apply the changes All three are removed by vpnrefre.sh at the end to make it clean

Requires: /scriptsubdirectory/.pfsensepassword - A bit of abstraction for the password
