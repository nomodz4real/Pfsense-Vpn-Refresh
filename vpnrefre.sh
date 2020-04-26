#!/bin/bash

# Grab the path of the script's directory
path=`pwd`

#Installing nordvpn-server-find if directory not found. 
#Hopefully I can convert to the website calls like in dejablues scripts
if [ ! -d $path/nordvpn-server-find ]
then
	git clone https://github.com/mrzool/nordvpn-server-find.git
fi

if [ `which pip3 | wc -l` = 0]
then
	echo "Pip3 not found, please install before continuing"
fi

# Find the US server with the least load using https://github.com/mrzool/nordvpn-server-find
bestserverfound=`$path/nordvpn-server-find/nordvpn-server-find -l US -c 10 -n 1 | grep .nordvpn.com | cut -d " " -f 1`

# Update the server to the one found by nordvpn-server-find
$path/tasks.py $bestserverfound

echo "Done!"