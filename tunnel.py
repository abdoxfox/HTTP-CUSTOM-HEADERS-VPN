import socket 
import time
import select
import threading
from inject import injector
import configparser
import ssl

bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'

class Tun(injector):
	def __init__(self):
		self.localip = '127.0.0.1'
		self.LISTEN_PORT = 9092

	def conf(self):
		config = configparser.ConfigParser()
		try:
			config.read_file(open('settings.ini'))
		except Exception as e:
			self.logs(e)
		return config
	def extraxt_sni(self,config):
		sni = config['sni']['server_name']
		return sni
	def proxy(self,config):
	    proxyhost = config['config']['proxyip']
	    proxyport = int(config['config']['proxyport'])
	    return [proxyhost,proxyport]
	def conn_mode(self,config):
		mode = config['mode']['connection_mode']
		return mode
	def tunneling(self,client,sockt):
		connected = True
		while connected == True:
			r, w, x = select.select([client,sockt], [], [client,sockt],3)
			print(r)
			if x: connected = False; break
			for i in r:
				try:
					data = i.recv(8192)
					if not data: connected = False; break
					if i is sockt:
						client.send(data)
					else:
						sockt.send(data)
				except:
					connected = False;break
		client.close()
		sockt.close()
		self.logs(R+'Disconnected '+GR)
	def destination(self,client, address):
	    try:
	        self.logs(G+'<#> Client {} received!{}'.format(address[-1],GR)) 
	        request = client.recv(9124).decode()
	        host = request.split(':')[0].split()[-1]
	        port = request.split(':')[-1].split()[0]
	        try:
	            proxip=self.proxy(self.conf())[0] 
	            proxport=self.proxy(self.conf())[1]
	        except ValueError:
	        	proxip = host
	        	proxport = port
	        (soc_f,soc_t,proto,_,add) = socket.getaddrinfo(proxip,proxport)[0]
	        s = socket.socket(soc_f,soc_t,proto)
	        s.connect(add)
	        self.logs(f'{G}connected to {add[0]}:{add[1]}{GR}')
	        if int(self.conn_mode(self.conf())) == 2:
	        	SNI_HOST = self.extraxt_sni(self.conf())
	        	ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
	        	s = ctx.wrap_socket(s, server_hostname=str(SNI_HOST))
	        	
	        elif int(self.conn_mode(self.conf())) == 3:
	        	SNI_HOST = self.extraxt_sni(self.conf())
	        	ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
	        	s = ctx.wrap_socket(s, server_hostname=str(SNI_HOST))
	        	injector.connection(self,client, s,str(add[0]),str(add[1]))
	        else:
	        	injector.connection(self,client, s,str(add[0]),str(add[1]))


	        self.tunneling(client,s)
	    except Exception as e:
	    	self.logs(f'{G}{e}{GR}')
	def create_connection(self):
		try:
		    sockt = socket.socket()
		    sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		    sockt.bind(('', self.LISTEN_PORT))
		    sockt.listen(0)
		    
		    self.logs('Waiting for incoming connection to : {}:{}\n'.format(self.localip,self.LISTEN_PORT))
		except OSError:
		    self.logs(O+'Port already used by another process\nRun script again'+GR)
		    
		    
		    
		while True:
		    try:
		        client, address = sockt.accept()
		        thr = threading.Thread(target=self.destination, args=(client, address))
		        thr.start()
		        
		    except KeyboardInterrupt:
		        sockt.close()
		        
		        
		sockt.close()
	def logs(self,log):
		logtime = str(time.ctime()).split()[3]
		logfile = open('logs.txt','a')
		logfile.write(f'[{logtime}] : {str(log)}\n')
if __name__=='__main__':
	start = Tun()
	start.create_connection()