import subprocess
import os
def handler():
    print('killing process ...')
    cmd = subprocess.Popen(("sudo netstat -anp|grep screen|awk '{print$9}'"),shell=True, stdout=subprocess.PIPE)
    output, error = cmd.communicate()
    for line in output.splitlines():
            pid = line.split(b'/')[0].decode()
            os.system(f'kill {pid}')

handler()
