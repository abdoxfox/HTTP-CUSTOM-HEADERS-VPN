#!/bin/bash

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'
cat << EOF > redsocksSetup.sh
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'
if [ -d "redsocks/" ]   
then 
echo "${GREEN}Redsocks installed ${SCOLOR}"
else
echo -e "${GREEN} COMPILLING REDSOCKS BINARY ...${SCOLOR}"
sleep 1
unzip redsocks 
cd redsocks 
make
chmod +x redsocks
fi 
EOF
bash redsocksSetup.sh && rm redsocksSettup.sh
clear

echo -e "${GREEN}Choose Connection Method:"
echo "0 - SSH Direct "
echo "1 - PAYLOAD "
echo "2 - SSL "
echo -e "3 - SSL+PAYLOAD "

read -p "Enter choice number : " mode
echo -e " ${GREEN}Enable ssh compression [y/n]"
read -p ": " enable
find=`cat settings.ini | grep "connection_mode = " |awk '{print $3}'`

sed -i "s/connection_mode = $find/connection_mode = $mode/g" settings.ini
value=`cat settings.ini | grep "enable_compression = " | awk '{print $3}'`

sed -i "s/enable_compression = $value/enable_compression = $enable/g" settings.ini
sleep 1

killprocess() {
echo -e "${RED} KILLING PROCESS...." 
python3 pidkill.py >>/dev/null 
rm -rf logs.txt
echo -e " DONE ${SCOLOR}"
}

function connect() {
        localport="$1"
	screen -AmdS nohub python3 tunnel.py $localport
	sleep 1
	if [ "$mode" = '0' ] || [ "$mode" = '1' ]
	then

		screen -AmdS nohub python3 ssh.py 1 $localport
	elif [ "$mode" = '2' ] || [ "$mode" = '3' ]
		then 
			
			screen -AmdS pythonwe python3 ssh.py 2  $localport 
	else
		echo -e "${RED}wrong choice\ntry again${SCOLOR}"
		killprocess
		exit
	fi

	echo -e "${YELLOW}---logs----${SCOLOR}"

	sleep 10
	cat logs.txt

	var=`cat logs.txt | grep "CONNECTED SUCCESSFULLY"|awk '{print $2}'`
	if [ "$var" = "SUCCESSFULLY" ];then 
		echo -e "${GREEN}---Tunneling  starts-----${SCOLOR}"
		chmod +x proxification
		sudo ./proxification >> /dev/null 
               
		iptables --flush
		
	else
		echo -e "${RED}Failed to connect ... Try again${SCOLOR}"
	fi
}
connect 9090
for i in {9091..9094}
do 
	
	killprocess
	echo -e "${GREEN}"
	read -p "reconnect ? [y\n] " reconnect
	if [ "$reconnect" = 'y' ]  || [ "$reconnect" = 'Y' ]
	then
          echo -e "reconnecting ${SCOLOR}"

		connect $i 
	else 
		exit
	fi 
done




