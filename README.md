# http-ssl-ssh-tunneling
http ssl ssh tunneling vpn for android and linux devices

# configuration :

past your data into file settings.ini 

![image](https://user-images.githubusercontent.com/46646744/120905618-2c1ee080-c64b-11eb-9ce8-fcc24da98004.png)

note : if are using leave the first part of settings.ini empty you have only te setup your ssh settings

# how it works!

note 1 : if you will use http or direct ssh connection :

[+] - chmod +x runvpn.sh

[=] - ./runvpn.sh 1    (argument 1 means that you will use payload / direct ssh connection)

note 2 : if are using ssl (sni bughost )

setup your sni bughost in settings.ini file and run the following command :

[+] - chmod +x runvpn.sh

[=] - ./runvpn.sh (argument 2 means that you will use ssl  method )


