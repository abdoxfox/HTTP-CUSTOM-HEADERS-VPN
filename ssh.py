import subprocess
import socket
import threading
import random
import time
import sys,os,re
import configparser

# colors
bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'

class sshRunn:
	def __init__(self,inject_port,):
		self.inject_host = '127.0.0.1'
		self.inject_port = inject_port
		self.connected = False
		

	def ssh_client(self,socks5_port,host,port,user,password,mode):
			try:
				
				dynamic_port_forwarding = '-CND {}'.format(socks5_port);threading.Lock().acquire()
				host = host 
				port = port
				username = user 
				password = password 
				inject_host= self.inject_host
				inject_port= self.inject_port
				nc_proxies_mode = [f'nc -X CONNECT -x {inject_host}:{inject_port} %h %p',f'corkscrew {inject_host} {inject_port} %h %p']
				arg = str(sys.argv[1])
				
				if arg == '2':
						proxycmd =f'-o "ProxyCommand={nc_proxies_mode[0]}"'
				elif arg =='1':
						proxycmd = f'-o "ProxyCommand={nc_proxies_mode[1]}"'
				elif arg =='0':
	   
					self.logs("Connecting Using Direct SSH " )
					proxycmd =''
				if self.enableCompress=='y':
					      compress = "-C"
				else:compress =""
				response = subprocess.Popen(
				(
	                   f'sshpass -p {password} ssh {compress} {proxycmd} {username}@{host} -p {port} -v {dynamic_port_forwarding} -o ConnectTimeout=3 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
	              ),
	             # timeout=5,
	              shell=True,
	              stdout=subprocess.PIPE,
	              stderr=subprocess.STDOUT)
				
				for line in response.stdout:
					line = line.decode('utf-8',errors='ignore')
					#print(line)
					
					if 'compat_banner: no match:' in line:
						self.logs(f"{G}handshake starts\nserver :{line.split(':')[2]}")
					elif 'Server host key' in line:self.logs(line)
					elif 'kex: algorithm:' in line:self.logs(line)
					elif 'kex: host key algorithm:' in line:self.logs(line)
					elif 'kex: server->client cipher:' in line:self.logs(line)
					 
					elif 'Next authentication method: password' in line:self.logs(G+'Authenticate to password'+GR)
					elif 'Authentication succeeded (password).' in line:self.logs('Authentication Comleted')
					elif 'pledge: proc' in line:
						self.logs(G+'CONNECTED SUCCESSFULLY '+GR)
						self.connected= True
					elif 'pledge: network' in line:
						self.logs(G+'CONNECTED SUCCESSFULLY '+GR)
						self.connected=True #os.system("chmod +x proxification && sudo bash proxification")
		   
					elif 'Permission denied' in line:self.logs(R+'username or password are inncorect '+GR)
					elif 'Connection closed' in line:self.logs(R+'Connection closed ' +GR)
					elif 'Could not request local forwarding' in line:self.logs(R+'Port used by another programs '+GR)
					#elif "client_loop: send disconnect:" in line:
					elif self.connected:
					    os.system("cat logs.txt && sudo bash proxification >/dev/null")
					    self.connected=False
					    return		
					
			except KeyboardInterrupt:
			    return 
			    
			if self.connected==False:
					    os.system('cat logs.txt')
			
	def create_connection(self,host,port,user,password,mode):
		global soc , payload
		try:
		    regx = r'[a-zA-Z0-9_]'
		    if re.match(regx,host):
		    	try:
		    		ip = socket.gethostbyname(host)
		    	except:
		  		  ip = host 						
		    sockslocalport  = 1080
		    return self.ssh_client(sockslocalport,ip,port,user,password,mode)
		    #sshthread = threading.Thread(target=self.ssh_client,args=(sockslocalport,ip,port,user,password,mode))
		   # sshthread.start()
		except ConnectionRefusedError:     
		    self.logs("CONNECTION REFUSED")	      
		except KeyboardInterrupt :
		    self.logs(R+'User Abort!'+GR)
		    
	def logs(self,log):
	   		with open('logs.txt','a') as file:
	   			file.write(log+'\n')
	
	def main(self):
		config = configparser.ConfigParser()
		config.read_file(open('settings.ini'))	
		host = config['ssh']['host']
		mode = config['mode']['connection_mode']
		port = config['ssh']['port']
		user = config['ssh']['username']
		password = config['ssh']['password']
		self.enableCompress = config['ssh']['enable_compression']
		self.create_connection(host,port,user,password,mode)
	

localport= sys.argv[2]
start = sshRunn(localport)
start.main()
		

