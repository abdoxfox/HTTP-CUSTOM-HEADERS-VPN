import subprocess
import os
def handler():
    print('killing process ...')
    cmd = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = cmd.communicate()
    target_process = "python"
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split()[0])
            os.system(f'kill {pid}')

handler()
