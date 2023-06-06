# ip netns exec NetNsA scp /path-to-file-to-copy/file.pdf rpi@192.168.2.1:destination-path

#run command - sudo python3 elephant.py

import time
import subprocess

if __name__ == "__main__":
    file = '500MB.9'
    startTime = time.time()
    scpCmd = 'ip netns exec NetNsA sshpass -p "root" scp /home/rpi/Desktop/NetNsA/' + file + ' rpi@192.168.2.1:/home/rpi/Desktop/NetNsB/' + file
    scpElephantProcess = subprocess.Popen(scpCmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
    scpElephantProcess.communicate()
    endTime = time.time()
    executionTime = endTime - startTime
    print("File Size = {}, ExecutionTime = {}".format(file, executionTime))
