#!/bin/bash
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'


argv=$1

if [ $argv = '1' ]; then 
	screen -AmdS nohub python http_direct_injector.py
	
else
	screen -AmdS nohub python sni.py 
fi
sleep 1
screen -AmdS nohub python ssh.py 
echo -e "${YELLOW}---logs----${SCOLOR}"
sleep 5
cat logs.txt
cat sshlogs.txt

var=`cat sshlogs.txt | grep "CONNECTED SUCCESSFULLY"|awk '{print $4}'`
if [ "$var" = "SUCCESSFULLY" ];then 
	echo -e "${GREEN}---Tunneling  starts-----"
	chmod +x proxification
	./proxification > /dev/null
	echo -e "${SCOLOR}"
	
else
	echo -e "${RED}something wrong with your settings"
	echo -e "check settings.ini file again ${SCOLOR}"
fi
echo -e "${RED} vpn service stopped" 
python pidkill.py
iptables --flush 
rm logs.txt
rm sshlogs.txt
echo -e "exiting ${SCOLOR}"
