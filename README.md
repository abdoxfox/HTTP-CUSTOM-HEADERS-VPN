
# HTTP TLS/SSL Tunneling Client for Linux (CLI)

A tool used to establish secure connections between a client and a server over an insecure network with customized header.

## Installation
Install dependencies:
```bash
apt install -y git openssh-client redsocks sshpass netcat-openbsd corkscrew screen python3 python3-pip
pip3 install certifi
```
Clone the repository:
```bash
git clone https://github.com/akilaid/HTTP-CUSTOM-HEADERS-VPN.git
```
stop and disable redsocks autostart on reboot:
```bash
systemctl stop redsocks
systemctl disable redsocks
```
Add your server seetings, custom payload and proxy (if required):
```bash
cd HTTP-CUSTOM-HEADERS-VPN
nano seetings.ini
```
Make it executable:
```bash
chmod +x runvpn.sh
```
Start VPN Client:
```bash
./runvpn.sh
```
## Authors
- [@abdoxfox](https://github.com/abdoxfox)
- [@Sewmina7](https://github.com/Sewmina7)
