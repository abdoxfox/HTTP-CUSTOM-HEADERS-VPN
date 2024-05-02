import subprocess
import socket
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
	def __init__(self,inject_port):
		self.inject_host = '127.0.0.1'
		self.inject_port = inject_port
		self.connected = None
		self.path = os.path.abspath(os.path.curdir)
	
	def LogServeMsg(self,lines):
	    slicemsg = lines[lines.index("debug1: SSH2_MSG_SERVICE_ACCEPT received\r\n") : lines.index('debug1: Next authentication method: publickey\r\n')]
	    msg = "".join(x for x in slicemsg)
	    self.logs(msg)
	        
	def ssh_client(self,host,port,password,mode,auth_methode):
			try:
				socks5_port = 1080
				dynamic_port_forwarding = '-CND {}'.format(socks5_port)	
				inject_host= self.inject_host
				inject_port= self.inject_port
				nc_proxies_mode = [f'nc -X CONNECT -x {inject_host}:{inject_port} %h %p',f'corkscrew {inject_host} {inject_port} %h %p']
				
				
				if mode in ("1","3"):
						proxycmd =f'-o "ProxyCommand={nc_proxies_mode[0]}"'
				elif mode =='2':
						proxycmd = f'-o "ProxyCommand={nc_proxies_mode[1]}"'
				elif mode =='0':
					self.logs("Connecting Using Direct SSH " )
					proxycmd =''
				if self.enableCompress=='y':
					      compress = "-C"
				else:
				    compress =""
				if str(auth_methode) == "publickey":  
				    sshcmd = f"ssh -i {password} cfgs/publickey.pem {proxycmd} useless@{host}"
				else:
				    sshcmd = f"sshpass -p {password} ssh {proxycmd} -F configFile host1"
				response = subprocess.Popen(
				(
	                   f'{sshcmd} {compress} -p {port} -v {dynamic_port_forwarding} -o ConnectTimeout=3 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
	              ),
	              shell=True,
	              stdout=subprocess.PIPE,
	              stderr=subprocess.STDOUT)
				for line in response.stdout:
					line = line.decode('utf-8',errors='ignore')
					
					if 'compat_banner: no match:' in line:
						self.logs(f"{G}handshake starts\nserver :{line.split(':')[2]}")
					elif 'Server host key' in line:self.logs(line)
					elif 'kex: algorithm:' in line:self.logs(line)
					elif 'kex: host key algorithm:' in line:self.logs(line)
					elif 'kex: server->client cipher:' in line:self.logs(line)
					elif 'Next authentication method: password' in line:self.logs(G+'Authenticate to password'+GR)
					elif 'Authentication succeeded (password).' in line:self.logs('Authentication Comleted')
					elif 'Permission denied' in line:self.logs(R+'username or password are inncorect '+GR)
					elif 'Connection closed' in line:self.logs(R+'Connection closed ' +GR)
					elif 'Could not request local forwarding' in line:self.logs(R+'Port used by another programs '+GR)
					elif "Next authentication method: publickey" in line:
					    self.logs(line)
					elif 'Entering interactive session.' in line:
					    self.logs(f'{G}connected{GR}')
					    self.connected=True
					
					if self.connected:
					    os.system("bash vpn/proxification > /dev/null &")
					    self.connected=False
					  	
			except KeyboardInterrupt:
			    return None
			except Exception as error:
			    print(error)
	def createConf(self,host,user):
			_=subprocess.run(["sh","ConfMake",host,user])
			
	def create_connection(self,host,port,user,password,mode,auth_methode ):
		try:
		    regx = r'[a-zA-Z0-9_]'
		    if self.proxy[0] :
		        remote_addr = self.proxy
		    else:
		        remote_addr = (host,port)
		    if mode in ("1" ,"3"):
		        payload = self.payload.replace("[host]",host)
		    else:
		        payload = ""
		    if self.sni:
		        self.logs(f"SNI : {O}{self.sni}{GR}")
		    self.logs(f"Connected to : {O}{remote_addr}\n{GR}sending Payload :{O}{payload}{GR}")
		    
		    if re.match(regx,host):
		    	try:
		    		host = socket.gethostbyname(host)
		    	except:
		  		  pass
		  		  
		    self.createConf(host,user)					
		    
		    self.ssh_client(host,port,password,mode, auth_methode)
		    
		except ConnectionRefusedError:     
		    self.logs("CONNECTION REFUSED")
		except Exception as e:
		    print(e)    
		
		    
	def logs(self,log):
		logtime = str(time.ctime()).split()[3]
		logfile = open('logs.txt','a')
		logfile.write(f'[{logtime}] : {str(log)}\n')
		print(f'[{logtime}] : {str(log)}')
	
	def main(self):
        
		currentdir = os.path.abspath(os.path.curdir)
		config = configparser.ConfigParser()
		config.read_file(open(f'{currentdir}/cfgs/settings.ini'))	
		host = config['ssh']['host']
		mode = config['mode']['connection_mode']
		port = config['ssh']['port']
		user = config['ssh']['username']
		password = config['ssh']['password']
		self.enableCompress = config['ssh']['enable_compression']
		auth_methode = config['ssh']['auth_methode']
		
		self.payload = config['Payload']['payload']
		self.proxy =(config['Payload']['proxyip'],config['Payload']['proxyport'])
		if mode in ("2" , "3"):
		    self.sni = config['sni']['server_name']
		else:
		    self.sni = False
		self.create_connection(host,port,user,password,mode,auth_methode)
    
	

localport= sys.argv[1]
start = sshRunn(localport)
start.main()

