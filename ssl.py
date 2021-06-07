import random
import ssl
import time
import sys
import socket, threading, select
import os
import subprocess
import configparser


bg=''
G = bg+'\033[32m'
O = bg+'\033[33m'
GR = bg+'\033[37m'
R = bg+'\033[31m'
logo='''

                        ++++  ++++   +++     ++++   +        +
                        +  +  +   +  +   +   +  +     +    +
                        ++++  +++    +   +   +  +       + 
                        +  +  +   +  +   +   +  +     +   +
                        +  +  ++++   + +     ++++   +       +
                        
                                #Github : https://github.com/abdoxfox
                                
            
    '''

def logs(log):
        logtime = str(time.ctime()).split()[3]
        logfile = open('logs.txt','a')
        logfile.write(f'[{logtime}] : {str(log)}\n')

def welcoming(str):
    	color=[bg,R,O,GR]
    	for n in str+ '\n':
    		logs(random.choice(color),end='')
    		sys.stdout.write(n)
    		sys.stdout.flush()
    		time.sleep(0.01)
#welcoming(logo)

config = configparser.ConfigParser()
try:
    config.read_file(open('settings.ini'))
except Exception as e:
    logs(f'{R}ERROR {e}')
    sys.exit()

LISTEN_PORT = '9092'
SNI_HOST = config['sni']['server_name']

def handler():
    logs('killing process ...')
    cmd = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = cmd.communicate()
    target_process = "python"
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            os.system(f'kill pid {pid}')



def conection(c, a):
    try:
         logs('<#> Client {} received!'.format(a[-1]))
         request = c.recv(9124).decode()
         print(request)
         host = request.split(':')[0].split()[-1]
         port = request.split(':')[-1].split()[0]
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
         s.connect((str(host), int(port)))
         logs(f'{G}connected to {host}:{port}{GR}')
         ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
         s = ctx.wrap_socket(s, server_hostname=str(SNI_HOST))
    	#logs(s)
    	# Direct
         c.send(b"HTTP/1.1 200 ABDOXFOX\nPython_crazy_coder\r\n\r\n")
    
         connected = True
         while connected == True:
        		r, w, x = select.select([c,s], [], [c,s], 3)
        		
        		if x: connected = False; break
        		for i in r:
        			try:
        				# Break if not data.
        				data = i.recv(19192)
        				if not data: connected = False; break
        				if i is s:
        					# Download.
        					c.send(data)
        				else:
        					# Upload.
        					s.send(data)
        			except:
        				connected = False
        				break
         c.close()
         s.close()
      
         logs(R+'<#> Client {} Disconnected {}'.format(a[-1],GR))
         
    except Exception as e:
        logs(f'{R}ERROR : {e}{GR}')

try:
    l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    l.bind(('', int(LISTEN_PORT)))
    l.listen(0)
    logs('Waiting for incoming connection to : 127.0.0.1:{}\n'.format(LISTEN_PORT))
except OSError:
    logs(O+'Port used \nRun script again'+GR)
    handler()
    
while True:
	try:
	    c, a = l.accept()
	    thr=threading.Thread(target=conection, args=(c, a))
	    thr.start()
	    
	except KeyboardInterrupt:
	    logs('CTRL + C  Pressed')
	    l.close()
	    handler()
	
	    
l.close()
