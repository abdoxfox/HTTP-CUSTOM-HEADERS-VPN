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
if command -v redsocks >/dev/null
then 
echo "${GREEN}Redsocks installed ${SCOLOR}"
else
echo -e "${GREEN} COMPILLING REDSOCKS BINARY & Dns2socks  ...${SCOLOR}"
sleep 1
unzip libs/redsocks 
cd redsocks 
make
mv redsocks ../redsocks
cp redsocks "$PREFIX"/bin
cd ..
fi
if ! command -v dns2socks >/dev/null
then
unzip libs/dns2socks.zip
cd dns2socks
make
cp dns2socks "$PREFIX"/bin
sleep 3
fi
cd ..
rm -rf redsocks/
rm -rf dns2socks/

EOF

bash rSetup.sh
rm rSetup.sh



clear


mode=$(cat cfgs/settings.ini |grep "connection_mode"| awk '{print $3}')

killprocess() {
echo -e "${RED}[+] KILLING PROCESS...." 
sudo pkill ssh
sudo pkill redsocks
sudo pkill dns2socks
sudo pkill screen

echo -e "[+] DONE ${SCOLOR}"
}
function serverlistening() {
    localport="$1"
    screen -AmdS nohup python3 __init__.py $localport
}
function connect() {
        localport="$1"

	if [ $mode = 0 ] 
        then
           python3 src/ssh.py 0 _
        elif [ $mode = "1" ] || [ $mode = "3" ]
	  then
               python3 src/ssh.py 1 $localport
	elif [ "$mode" = '2' ] 
		then 
			
			python3 src/ssh.py 2  $localport 
	else
	  echo "${RED}mode ${mode} is not listed ${SCOLOR} "
		exit
	fi
	
	
	
}
for i in {9000..9999}
do 
    clear
    echo "$GREEN ++++ LOGS ++++$SCOLOR"
	rm -rf logs.txt
	serverlistening $i
	sleep 1
	connect $i 
    killprocess
    sudo iptables -t nat -F
    sudo iptables -t nat -X
done

