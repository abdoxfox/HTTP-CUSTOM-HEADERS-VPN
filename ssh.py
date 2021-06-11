import subprocess
import socket
import select
import threading
import random
import time
import sys,os
import platform
import configparser

# colors
bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'

class sshRunn:
	def __init__(self,inject_host,inject_port):
		self.inject_host = inject_host
		self.inject_port = inject_port

	def ssh_client(self,socks5_port,host,port,user,password):
			try:
				
				dynamic_port_forwarding = '-CND {}'.format(socks5_port)
				host = host 
				port = port
				
				username = user 
				password = password 
				inject_host= self.inject_host
				inject_port= self.inject_port
				nc_proxies_mode = [f'corkscrew {inject_host} {inject_port} %h %p', f'nc -X CONNECT -x {inject_host}:{inject_port} %h %p']
				arg = str(sys.argv[1])
				if arg == '1':
					nc_proxy = nc_proxies_mode[0]
				else:
					nc_proxy = nc_proxies_mode[1]
				
				response = subprocess.Popen(
	                (
	                   f'sshpass -p {password} ssh -o "ProxyCommand={nc_proxy}" {username}@{host} -p {port} -v {dynamic_port_forwarding} ' + '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
	                   
	                
	                ),
	                shell=True,
	                stdout=subprocess.PIPE,
	                stderr=subprocess.STDOUT
	            )
				
				for line in response.stdout:
					line = line.decode('utf-8',errors='ignore').lstrip(r'(debug1|Warning):').strip() + '\r'
					self.logs(line)
					if 'pledge: proc' in line:self.logs(G+'CONNECTED SUCCESSFULLY '+GR)
					elif 'Permission denied' in line:self.logs(R+'username or password are incorrect'+GR)
					elif 'Connection closed' in line:self.logs(R+'Connection closed'+GR)
					elif 'Could not request local forwarding' in line:self.logs(R+'Port used by another programs'+GR)
			
			except KeyboardInterrupt:
				sys.exit('stoping ..')


	def create_connection(self,host,port,user,password):
		global soc , payload
		try:    								
		    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		    soc.connect((self.inject_host,int(self.inject_port)))
		    thread=threading.Thread(target=self.ssh_client,args=('1080',host,port,user,password))
		    thread.start()
		except ConnectionRefusedError:            
		    self.logs(R+'try run again again'+GR)
		    soc.close()
		      
		except KeyboardInterrupt:
				self.logs(R+'ssh stopped'+GR)

	def logs(self,log):
		logtime = str(time.ctime()).split()[3]
		logfile = open('sshlogs.txt','a')
		logfile.write(f'[{logtime}] : {str(log)}\n')
if __name__=='__main__':		        
	
	
	
	start = sshRunn('127.0.0.1','9092')
	config = configparser.ConfigParser()
	try:
		config.read_file(open('settings.ini'))
	except Exception as e:
		start.logs(f'{R}ERROR {e}')
		sys.exit()
	
	host = config['ssh']['host']
	port = config['ssh']['port']
	user = config['ssh']['username']
	password = config['ssh']['password']
	if host:
		start.create_connection(host,port,user,password) 
	else:
		start.logs(f'{R}ssh field is empty in file  settings.ini {GR}')
		sys.exit
	
