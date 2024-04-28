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
pkill ssh
pkill redsocks
pkill dns2socks
echo -e "[+] DONE ${SCOLOR}"
}
function serverlistening() {
    localport="$1"
    python3 main.py $localport & 
    echo ""
}
function connect() {
        localport="$1"

	if [ $mode = 0 ] 
        then
           python3 src/ssh.py 0
    else
			
			python3 src/ssh.py $localport 
	
	fi
	
}

OnExit() {
    lport=$1
    pid=$(sudo netstat -anp|grep "$lport" | awk '{print$7}' | grep "python3"|sed -e 's/\/python3//g'|tail -1)
    kill $pid
    echo -e "${RED}Disconnected ${SCOLOR}"

}

for i in {9008..9999}
do 
    
    echo -e "$GREEN ++++ LOGS ++++$SCOLOR"
	rm -rf logs.txt
	serverlistening $i
	sleep 1
	connect $i
    killprocess $i
    signal=$(($i+1))  
    trap "OnExit $signal" EXIT
done

T
