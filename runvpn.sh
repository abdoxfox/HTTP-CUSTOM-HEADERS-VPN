#!/bin/bash
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'


echo -e "${GREEN}Choose Connection Method:"
echo "0 - SSH Direct "
echo "1 - PAYLOAD "
echo "2 - SSL "
echo -e "3 - SSL+PAYLOAD \nEnter choice number :${SCOLOR}"

read  mode
find=`cat settings.ini | grep "connection_mode = " |awk '{print $3}'`

sed -i "s/connection_mode = $find/connection_mode = $mode/g" settings.ini

sleep 1
screen -AmdS nohub python tunnel.py
sleep 1
if [ "$mode" = '0' ] || [ "$mode" = '1' ]
then

	screen -AmdS nohub python ssh.py 1
elif [ "$mode" = '2' ] || [ "$mode" = '3' ]
	then 
		
		screen -AmdS nohub python ssh.py 2
else
	echo -e "${RED}wrong choice\ntry again${SCOLOR}"
	python pidkill.py
	exit
fi
echo -e "${YELLOW}---logs----${SCOLOR}"

sleep 10
cat logs.txt

var=`cat logs.txt | grep "CONNECTED SUCCESSFULLY"|awk '{print $4}'`
if [ "$var" = "SUCCESSFULLY" ];then 
	echo -e "${GREEN}---Tunneling  starts-----"
	chmod +x proxification
	./proxification > /dev/null
	echo -e "${SCOLOR}"
	iptables --flush
	
else
	echo -e "${RED}failed! , check settings.ini file again ${SCOLOR}"
fi

echo -e "${RED} vpn service stopped" 
python pidkill.py 
rm logs.txt
echo -e "exiting ${SCOLOR}"


