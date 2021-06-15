#!/bin/bash
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'


argv=$1

if [ "$argv" = '1' ]; then 
	screen -AmdS nohub python http_direct_injector.py
	sleep 3
	screen -AmdS nohub python ssh.py 1
	
else
	echo -e "${GREEN}Default mode is sni \n to use payload choice type : \n./runvpn.sh 1${SCOLOR}"
	screen -AmdS nohub python sni.py 
	sleep 3
	screen -AmdS nohub python ssh.py 2
fi

echo -e "${YELLOW}---logs----${SCOLOR}"

sleep 10
cat logs.txt
sshlog="sshlogs.txt"
if [ -f "$sshlog" ]; then 
	cat sshlogs.txt
else
	echo "${RED}Not connected ${SCOLOR}"
	screen -AmdS nohub python pidkill.py
	rm logs.txt
	exit
fi

var=`cat sshlogs.txt | grep "CONNECTED SUCCESSFULLY"|awk '{print $4}'`
if [ "$var" = "SUCCESSFULLY" ];then 
	echo -e "${GREEN}---Tunneling  starts-----"
	chmod +x proxification
	./proxification > /dev/null
	iptables --flush 
	echo -e "${SCOLOR}"
	
else
	echo -e "${RED}failed! , check settings.ini file again ${SCOLOR}"
fi

echo -e "${RED} vpn service stopped" 
python pidkill.py
rm logs.txt
rm sshlogs.txt
echo -e "exiting ${SCOLOR}"
