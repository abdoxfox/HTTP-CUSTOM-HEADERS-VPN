import socket 
import time
import select
import threading
from inject import injector
import configparser
import ssl,os,certifi,sys

bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'
Buffer_lenght = 4096 * 4

class Tun(injector):
	def __init__(self):
		self.localip = '127.0.0.1'
		self.LISTEN_PORT = int(sys.argv[1])

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
		
	def gethost(self,config):
		host=config['ssh']['host']
		return host
		
	def proxy(self,config):
	    proxyhost = config['config']['proxyip']
	    proxyport = int(config['config']['proxyport'])
	    return [proxyhost,proxyport]
	    
	def conn_mode(self,config):
		mode = config['mode']['connection_mode']
		return mode
		
	def tunneling(self,client,sockt,packet):
		client.send(packet)
		connected = True
		while connected == True:
			r, _, x = select.select([client,sockt], [], [client,sockt],3)
			if x: connected = False; break
			for i in r:
				try:
					data = i.recv(Buffer_lenght)
					if not data: connected = False;break 
					if i is sockt:
						client.send(data)
					else:
						sockt.send(data)
				except Exception as e:
					self.logs(f'{R} {e}{GR}')
					connected = False;break
		client.close()
		sockt.close()
		os.system('sudo pkill redsocks')
		
	def destination(self,client, address):
	    mode = int(self.conn_mode(self.conf()))
	    try:
	        #self.logs(G+'<#> Client {} received!{}'.format(address[-1],GR)) 
	        request = client.recv(1024).decode()
	        host = self.gethost(self.conf())
	        port = request.split(':')[-1].split()[0]
	        try:
	            proxip=self.proxy(self.conf())[0] 
	            proxport=self.proxy(self.conf())[1]
	        except ValueError:
	        	proxip = host
	        	proxport = port
	        sockt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	        sockt.settimeout(10)
	        sockt.connect((proxip,int(proxport)))
	        self.logs(f'{O}[TCP] {G}connected to {proxip}:{proxport}{GR}')
	       
	        if mode == 2 or mode == 3  :
	        	SNI_HOST = self.extraxt_sni(self.conf())
	        	context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	        	sockt = context.wrap_socket(sockt,server_hostname=str(SNI_HOST))
	        	context.verify_mode  = ssl.CERT_REQUIRED
	        	context.load_verify_locations(
	        	cafile=os.path.relpath(certifi.where()),
	        	capath=None,cadata=None)
	        	self.logs(f'Handshaked successfully to {SNI_HOST}')
	        	try:
	        		self.logs(f'''{O}[TCP] Protocol :{G}{sockt.version()}\n{O}Ciphersuite :{G} {sockt.cipher()[0]}\n{O}Peerprincipal:{G} C={sockt.getpeercert()["subject"][1][0][1]}, ST={sockt.getpeercert()["subject"][1][0][1]} , L={sockt.getpeercert()["subject"][2][0][1]} , O={sockt.getpeercert()["subject"][3][0][1]} , CN={sockt.getpeercert()["subject"][4][0][1]}  {GR}''')
	        	except:
	        		self.logs(f'''{O}[TCP] Protocol :{G}{sockt.version()}\n{O}Ciphersuite :{G} {sockt.cipher()[0]}\n{O}Peerprincipal:{G} {sockt.getpeercert()["subject"]}''')
	        	
	        if mode == 2:
	        	client.send(b"HTTP/1.1 200 OK\r\n\r\n")
	        packet = injector.connection(self,client, sockt,str(host),str(port))
	        if packet:
	        	self.tunneling(client,sockt,packet)
	    except Exception as e:
	    	self.logs(f'{e}')
	def create_connection(self):
	    
	    for res in socket.getaddrinfo(self.localip, self.LISTEN_PORT, socket.AF_UNSPEC,socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
	        af, socktype, proto, canonname, sa = res
	        try:
	            sockt = socket.socket(af, socktype, proto)
	        except OSError as msg:
	            self.logs(str(msg))
	            continue
	        try:
	           localAddress = socket.gethostbyname("localhost")
	           sockt.bind((localAddress,self.LISTEN_PORT))
	           sockt.listen(1)
	        except OSError as msg:
	            self.logs(str(msg))
	            sockt.close()
                    
	        if sockt:
	          pass
	        self.logs('Waiting for incoming connection to : {}:{}\n'.format(self.localip,self.LISTEN_PORT))
	        while True:
		        try:
		           client, address = sockt.accept()
		           self.destination(client,address)
		        except :
		           sockt.close()
		           break
		       
	def logs(self,log):
		logtime = str(time.ctime()).split()[3]
		logfile = open('logs.txt','a')
		logfile.write(f'[{logtime}] : {str(log)}\n')
if __name__=='__main__':
	start = Tun()
	start.create_connection()


