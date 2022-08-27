import subprocess
import os
def handler():
    print('killing process ...')
    screens = subprocess.Popen(["screen", "-ls"], stdout=subprocess.PIPE)
    output, error = screens.communicate()
    target_process1 = "tunnel.py"
    target_process2 = "ssh.py"
    for line in output.splitlines():
        if target_process1 in str(line) or target_process2 in str(line):
            print(line)
            pid = int(str(line).split("t")[1].split(".")[0])
            print(pid)
            os.system(f'kill {pid}')

handler()
