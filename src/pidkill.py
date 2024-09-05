import subprocess
import os

def handler(thread):
    cmd = subprocess.Popen((f"netstat -anp|grep {thread}"+"|awk '{print$7}'"),shell=True, stdout=subprocess.PIPE)
    output, error = cmd.communicate()
    for line in output.splitlines():
            pid = line.split(b'/')[0].decode()
            os.system(f'kill {pid}')


