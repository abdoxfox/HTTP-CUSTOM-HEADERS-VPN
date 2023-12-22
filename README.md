# What's New:
* added dns2socks for resolve dns udp traffic over cloudflare dns 
* change tunneling mode is only on settings.ini file

let me now if did you had some other issues to fix by opening a new issue.

# HTTP CUSTOM HEADERS VPN 
is an ssh based vpn that uses:

- HTTP Headers (payload) direct or with proxy.
- SSL/TLS Handshake over SNI.
- Combination between both (payload + ssl ) is supported too.




# packages :

```
apt install -y git openssh sshpass netcat-openbsd corkscrew screen python3
apt install python3-pip 
apt install make
pip install certifi
```


# how it works!

(root is required in android )
```
git clone https://github.com/abdoxfox/HTTP-CUSTOM-HEADERS-VPN.git
cd HTTP-CUSTOM-HEADERS-VPN
```
[+] - and fill the `cfgs/settings.ini` file:
* choose your connection mode:

    mode 0 : ssh direct

    mode 1 : payload with or without proxy

    mode 2 :  ssl/tls (sni)

     mode 3 : payload + sni 

- according to your mode preference modify below line in settings.ini with the choosen mode number
ex
connection_mode = 0

![image](https://user-images.githubusercontent.com/46646744/122469251-9f621400-cfb4-11eb-9d64-f5dbfa2dffa9.png)


- then:
```
chmod +x runvpn.sh
sudo bash runvpn.sh
```


# screenshot

![image](https://user-images.githubusercontent.com/46646744/121225010-00853b80-c881-11eb-8cb6-4fcea95f8f88.png)

* note : to stop the script press CTRL + C

![image](https://user-images.githubusercontent.com/46646744/121225175-2c082600-c881-11eb-9c82-27fc2f4200a1.png)


