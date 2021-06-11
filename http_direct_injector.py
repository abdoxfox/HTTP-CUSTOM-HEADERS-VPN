import random
import time
import sys
import socket, threading, select
import os,signal
import json
import subprocess
import platform
import configparser

bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'



class injector:
	def __init__(self):
		self.LISTEN_PORT = '9092'	
		self.localip = '127.0.0.1'

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
	    
	def killpid(self):
		self.logs('killing process ...')
		cmd = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
		output, error = cmd.communicate()
		target_process = "python"
		for line in output.splitlines():
		    if target_process in str(line):
		        pid = int(line.split(None, 1)[0])
		        os.system('kill pid '+str(pid))



	

	def payloadformating(self,payload,host,port):
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

	def connection(self,client, address):
	    try:
	        self.logs('<#> Client {} received!'.format(address[-1])) 
	        request = client.recv(9124).decode()
	        host = request.split(':')[0].split()[-1]
	        port = request.split(':')[-1].split()[0]
	        try:
	            proxip=self.proxy(self.conf())[0] 
	            proxport=self.proxy(self.conf())[1]
	        except ValueError:
	        	proxip = host
	        	proxport = port
	        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	        s.connect((str(proxip), int(proxport)))
	        self.logs(f'{G}connected to  proxy {proxip}:{proxport}{GR}')
	        payload = self.payloadformating(self.getpayload(self.conf()),host,port)
	        if payload :
	        	payload = payload 
	        else:
	        	payload = f'CONNECT {host}:{port} HTTP/1.0'
	     
	        
	        if '[split]' in payload or '[instant_split]' in payload or '[delay_split]' in payload:
	          payload = payload.replace('[split]'        ,'||0.5||')
	          payload = payload.replace('[delay_split]'  ,'||1.5||')
	          payload = payload.replace('[instant_split]','||0.0||')
	          req = payload.split('||')
	          for payl in req:
	              if ('0.5' == payl or  '1.5' == payl or '0.0' == payl) :
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
	          s.send(payl[0].encode())
	          s.send(payl[0].encode())
	          s.send(payl[1].encode())

	        elif '[reverse_split]' in payload or '[x-split]' in payload:
	          payload = payload.replace('[reverse_split]','||2|')
	          payload = payload.replace('[x-split]','||2|')
	          req = payload.split('||')
	          payl = []
	          for element in req:
	            if element and element == '2':pass
	            else:payl.append(element)
	          s.send(payl[0].encode())
	          s.send(payl[1].encode())
	          s.send(payl[1].encode())

	        elif '[split-x]' in payload:
	          payload = payload.replace('[split-x]','||3||')
	          req = payload.split('||')
	          xsplit = []
	          for element in req:
	            if element and element == '3':pass
	            else:xsplit.append(element)
	          s.send(xsplit[0].encode())
	          s.send(xsplit[1].encode())
	          time.sleep(0.5)
	          s.send(xsplit[1].encode())

	        else:
	          
	          s.send(payload.encode())
	          status = s.recv(1024).split('\n'.encode())[0]
	          self.logs(f'status :{G} {status.decode()}{GR}' )
	        client.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")
	        connected = True
	        while connected == True:
	                r, w, x = select.select([client,s], [], [client,s],3)
	               
	                if x: connected = False; break
	                for i in r:
	                    try:
	                        
	                        data = i.recv(19192)
	                        if not data: connected = False; break
	                        if i is s:
	                  
	                            client.send(data)
	                        else:
	                            
	                            s.send(data)
	                    except Exception as e:
	                    	self.logs(f'Error : {e}')
	                    	connected = False;break
	        client.close()
	        s.close()
	        self.logs(R+'<#> Client {} Disconnected {}'.format(address[-1],GR))
	        
	    except Exception as e:
	        self.logs(f'{R}ERROR : {e}')

	def create_connection(self):
		try:
		    sockt = socket.socket()
		    sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		    sockt.bind(('', int(self.LISTEN_PORT)))
		    sockt.listen(0)
		    
		    self.logs('Waiting for incoming connection to : {}:{}\n'.format(self.localip,self.LISTEN_PORT))
		except OSError:
		    self.logs(O+'Port already used by another process\nRun script again'+GR)
		    self.killpid()
		    
		    
		while True:
		    try:
		        c, a = sockt.accept()
		        thr = threading.Thread(target=self.connection, args=(c, a))
		        thr.start()
		        
		    except KeyboardInterrupt:
		        sockt.close()
		        self.killpid()
		        
		sockt.close()
	def logs(self,log):
		logtime = str(time.ctime()).split()[3]
		logfile = open('logs.txt','a')
		logfile.write(f'[{logtime}] : {str(log)}\n')
if __name__=='__main__':
	start = injector()
	start.create_connection()
