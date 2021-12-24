import time
import socket 
import configparser
import re

bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'



class injector:
	def __init__(self):
		pass

	def conf(self):
		config = configparser.ConfigParser()
		try:
			config.read_file(open('settings.ini'))
		except Exception as e:
			self.logs(e)
		return config

	def getpayload(self,config):
		payload = config['config']['payload']
		return payload 

	def proxy(self,config):
	    proxyhost = config['config']['proxyip']
	    proxyport = int(config['config']['proxyport'])
	    return [proxyhost,proxyport]
	def conn_mode(self,config):
		mode = config['mode']['connection_mode']
		return mode

	def auto_rep(self,config):
		result = config['config']['auto_replace']
		return result


	def payloadformating(self,payload,host,port):
		self.logs(f'{O}[TCP] Sending payload :\n{payload}{GR}')
		payload = payload.replace('[crlf]','\r\n')
		payload = payload.replace('[crlf*2]','\r\n\r\n')
		payload = payload.replace('[cr]','\r')
		payload = payload.replace('[lf]','\n')
		payload = payload.replace('[protocol]','HTTP/1.0')
		payload = payload.replace('[ua]','Dalvik/2.1.0')  
		payload = payload.replace('[raw]','CONNECT '+host+':'+port+' HTTP/1.0\r\n\r\n')
		payload = payload.replace('[real_raw]','CONNECT '+host+':'+port+' HTTP/1.0\r\n\r\n') 
		payload = payload.replace('[netData]','CONNECT '+host+':'+port +' HTTP/1.0')
		payload = payload.replace('[realData]','CONNECT '+host+':'+port+' HTTP/1.0')               	
		payload = payload.replace('[split_delay]','[delay_split]')
		payload = payload.replace('[split_instant]','[instant_split]')
		payload = payload.replace('[method]','CONNECT')
		payload = payload.replace('mip','127.0.0.1')
		payload = payload.replace('[ssh]',host+':'+port)
		payload = payload.replace('[lfcr]','\n\r')
		payload = payload.replace('[host_port]',host+':'+port)
		payload = payload.replace('[host]',host)
		payload = payload.replace('[port]',port)
		payload = payload.replace('[auth]','')
		return payload

	def connection(self,client, s,host,port):
	        if int(self.conn_mode(self.conf())) == 0:
	        	payload = f'CONNECT {host}:{port} HTTP/1.0\r\n\r\n'
	       
	        else:
	        	payload = self.payloadformating(self.getpayload(self.conf()),host,port)
	        
	        if '[split]' in payload or '[instant_split]' in payload or '[delay_split]' in payload:
	          payload = payload.replace('[split]'        ,'||1.0||')
	          payload = payload.replace('[delay_split]'  ,'||1.5||')
	          payload = payload.replace('[instant_split]','||0.0||')
	          
	          req = payload.split('||')
	          
	          for payl in req:
	              if payl in ['1.0','1.5','0.0'] :
	                delay = payl
	                time.sleep(float(delay))
	              else:
	                s.send(payl.encode())
	        
	        elif '[repeat_split]' in payload  :
	          payload = payload.replace('[repeat_split]','||1||')
	          payload = payload.replace('[x-split]','||1||')
	          req = payload.split('||')
	          payl = []
	          for element in req:
	            if element and element == '1' :pass
	            else:payl.append(element)
	          rpspli = payl[0]+payl[0]
	          s.send(rpspli.encode())
	          s.send(payl[1].encode())

	        elif '[reverse_split]' in payload or '[x-split]' in payload:
	          payload = payload.replace('[reverse_split]','||2|')
	          payload = payload.replace('[x-split]','||2|')
	          req = payload.split('||')
	          payl = []
	          for element in req:
	            if element and element == '2':pass
	            else:payl.append(element)
	          rvsplit = payl[0]+payl[1]
	          s.send(rvsplit.encode())
	          s.send(payl[1].encode())

	        elif '[split-x]' in payload:
	          payload = payload.replace('[split-x]','||3||')
	          req = payload.split('||')
	          xsplit = []
	          for element in req:
	            if element and element == '3':pass
	            else:xsplit.append(element)
	          alpay = xsplit[0]+xsplit[1]
	          s.send(alpay.encode())
	          
	          time.sleep(1.0)
	          s.send(xsplit[1].encode())
	        else:
	          
	          s.send(payload.encode())
	        self.get_resp(s,client)
	def get_resp(self,server,client) :
		packet = server.recv(1024)
		res = packet.decode('utf-8','ignore')
		status = res.split('\n')[0]
		if status.split('-')[0]=='SSH':
			self.logs(f'{O}response : {G}{status}{GR}')
			client.send(packet)
			return True
		else:
			if re.match(r'HTTP/\d(\.\d)? \d\d\d ',status):
				self.logs(f'{O}response : {G}{status}{GR}')
			client.send(b'HTTP/1.1 200 Connection established\r\n\r\n')
			return self.get_resp(server,client)
		
	def logs(self,log):
		logtime = str(time.ctime()).split()[3]
		logfile = open('logs.txt','a')
		logfile.write(f'[{logtime}] : {str(log)}\n')
