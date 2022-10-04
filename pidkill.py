import subprocess
import os,sys
def handler():
    print('killing process ...')
    cmd = subprocess.Popen(("sudo netstat -anp|grep screen|awk '{print$9}'"),shell=True, stdout=subprocess.PIPE)
    output, error = cmd.communicate()
    for line in output.splitlines():
            pid = line.split(b'/')[0].decode()
            print(pid)
            os.system(f'kill {pid}')
try:
	if sys.argv[1] :
		os.system('su -c am start --user 0 -n com.termux/com.termux.app.TermuxActivity && sudo pkill bash >> /dev/null')
		os.system('sudo iptables -t nat -F OUTPUT')
		os.system('sudo rm logs.txt')
except:pass
handler()
