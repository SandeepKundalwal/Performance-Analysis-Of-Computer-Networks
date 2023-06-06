# ip netns exec NetNsA scp /path-to-file-to-copy/file.pdf rpi@192.168.2.1:destination-path

#run command - sudo python3 mouse.py <NmIndices> <FileIndices>

import sys
import time
import random
import subprocess

Nm = [5, 10, 15, 20]
mouse_files = ['1B.1', '10KB.3', '100KB.4', '500KB.5']

if __name__ == "__main__":
    N = Nm[int(sys.argv[1])]
    file = mouse_files[int(sys.argv[2])]
    executionTime = 0.00
    startTime = time.time()
    for i in range(N):
        scpCmd = 'ip netns exec NetNsA sshpass -p "root" scp /home/rpi/Desktop/NetNsA/' + file + ' rpi@192.168.2.1:/home/rpi/Desktop/NetNsB/' + str(i) + '_' + file
        scpMouseProcess = subprocess.Popen(scpCmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
        scpMouseProcess.communicate()
        time.sleep(random.expovariate(0.20))   
    endTime = time.time()
    executionTime = endTime - startTime
    print("File Size = {}, Nm = {}, ExecutionTime = {}".format(file, N, executionTime))
    
    
