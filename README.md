

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

# configuration :

past your data into file settings.ini 

![image](https://user-images.githubusercontent.com/46646744/122469251-9f621400-cfb4-11eb-9d64-f5dbfa2dffa9.png)


# how it works!

(root is required in android )
```
git clone https://github.com/abdoxfox/HTTP-CUSTOM-HEADERS-VPN.git
cd HTTP-CUSTOM-HEADERS-VPN
```
[+] - fill settings.ini file with your suitable configuration (look at sample configuration in image above)
- then:
```
chmod +x runvpn.sh
sudo bash runvpn.sh
```
* choose your connection mode:

![image](https://user-images.githubusercontent.com/46646744/122469828-48a90a00-cfb5-11eb-8b2b-48e9870618b2.png)


# screenshots 

![image](https://user-images.githubusercontent.com/46646744/121225010-00853b80-c881-11eb-8cb6-4fcea95f8f88.png)

* note : to stop the script press CTRL + C

![image](https://user-images.githubusercontent.com/46646744/121225175-2c082600-c881-11eb-9c82-27fc2f4200a1.png)


