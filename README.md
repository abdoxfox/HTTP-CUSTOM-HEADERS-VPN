# http-ssl-ssh-tunneling
http ssl ssh tunneling vpn for android and linux devices

# packages :

[+] - apt install -y git python openssh sshpass netcat-openbsd nmap-netcat

[+] - apt install screen 

# configuration :

past your data into file settings.ini 

![image](https://user-images.githubusercontent.com/46646744/120905618-2c1ee080-c64b-11eb-9ce8-fcc24da98004.png)

note : if are using Direct ssh leave the first part of settings.ini file empty you have only to setup your ssh settings

# how it works!

(root is required in android )

[+] - git clone https://github.com/abdoxfox/http-ssl-ssh-injector.git

# if you will use custom payload or direct ssh connection :

* setup yor custom payload and proxy (if need it  else leave it empty) and ssh details in settings.ini file.

[+] - cd http-ssl-ssh-injector

[+] - sudo  or tsu for termux  #run as root

[+] - chmod +x runvpn.sh

[+] - ./runvpn.sh 1          (argument 1 means that you will use payload / direct ssh connection)

 # if are using ssl (sni bughost )

* setup your sni bughost and ssh details in settings.ini file and run the following commands :

[+] - cd http-ssl-ssh-injector

[+] - sudo or tsu 

[+] - chmod +x runvpn.sh

[+] - ./runvpn.sh 2         (argument 2 means that you will use ssl  method )


# screenshots 

![image](https://user-images.githubusercontent.com/46646744/121225010-00853b80-c881-11eb-8cb6-4fcea95f8f88.png)

* note : to stop the script press CTRL + C

![image](https://user-images.githubusercontent.com/46646744/121225175-2c082600-c881-11eb-9c82-27fc2f4200a1.png)


screenshots from : @megasniff_v2 (thanks a lot bro)


