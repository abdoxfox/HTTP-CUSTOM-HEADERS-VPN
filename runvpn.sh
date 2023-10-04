#!/bin/bash

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'


cat << EOF > rSetup.sh
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
SCOLOR='\033[0m'
if [ -f "redsocksv" ] 
then 
echo "${GREEN}Redsocks installed ${SCOLOR}"
else
echo -e "${GREEN} COMPILLING REDSOCKS BINARY & Dns2socks  ...${SCOLOR}"
sleep 1
unzip redsocks 
cd redsocks 
make
mv redsocks ../redsocksv
cd ..
cp redsocksv "$PREFIX"/bin
unzip dns2socks.zip
cd dns2socks
make
chmod 777 dns2socks
cp dns2socks "$PREFIX"/bin
sleep 3
fi
rm -rf redsocks
rm -rf dns2socks
EOF

bash rSetup.sh
rm rSetup.sh

clear


mode=$(cat settings.ini |grep "connection_mode"| awk '{print $3}')

killprocess() {
echo -e "${RED}[+] KILLING PROCESS...." 
sudo pkill ssh
sudo pkill redsocksv
sudo pkill screen
echo -e "[+] DONE ${SCOLOR}"
}
function serverlistening() {
    localport="$1"
    screen -AmdS nohup python3 tunnel.py $localport
}
function connect() {
        localport="$1"

	if [ $mode = 0 ] 
        then
           python3 ssh.py 0 _
        elif [ $mode = "1" ] || [ $mode = "3" ]
	  then
               
               sleep 1
               python3 ssh.py 1 $localport
	elif [ "$mode" = '2' ] 
		then 
			
			python3 ssh.py 2  $localport 
	else
	  echo "${RED}mode ${mode} is not listed ${SCOLOR} "
		exit
	fi
	
	
	
}
for i in {9089..9099}
do 
	rm -rf logs.txt
	serverlistening $i
	sleep 1
	connect $i 
    killprocess
    sudo iptables -t nat -F
    sudo iptables -t nat -X
done

