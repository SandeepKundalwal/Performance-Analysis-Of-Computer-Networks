import subprocess

setup = [
    'ip netns add NetNsA',
    'ip netns add NetNsB',
    'ip -n NetNsA link add eth0 type veth peer name eth0 netns NetNsB',
    'ip -n NetNsA addr add 192.168.1.1/24 dev eth0',
    'ip -n NetNsB addr add 192.168.2.1/24 dev eth0',
    'ip netns exec NetNsA ip link set eth0 up',
    'ip netns exec NetNsB ip link set eth0 up',
    'ip netns exec NetNsA ip route add default via 192.168.1.1 dev eth0',
    'ip netns exec NetNsB ip route add default via 192.168.2.1 dev eth0'
]

queuingDisciplines = [
    'no-op',
    'ip netns exec NetNsA tc qdisc add dev eth0 root netem delay 50ms',
    'ip netns exec NetNsA tc qdisc add dev eth0 root netem delay 50ms 50ms'
]

teardown = [
    'ip netns del NetNsA',
    'ip netns del NetNsB'
]


def run_steps(setup_steps, ignore_errors=False):
    for step in setup_steps:
        try:
            print('+ {}'.format(step))
            subprocess.check_call(step, shell=True)
        except subprocess.CalledProcessError:
            if ignore_errors:
                pass
            else:
                raise

if __name__ == '__main__':
    try:
        run_steps(setup)
        
        iteration = 1
        pingCmd = "ip netns exec NetNsA ping -c 4 192.168.2.1"
        delQueuingDisciplineCmd = "ip netns exec NetNsA tc qdisc del dev eth0 root"

        for queuingDiscipline in queuingDisciplines:
            avgs = []
            print(queuingDiscipline)
            
            if iteration == 3:
                subprocess.Popen(delQueuingDisciplineCmd, shell=True)
                
            discipline = subprocess.Popen(queuingDiscipline, shell=True)
            
            for i in range(10):
                pingOutput = subprocess.Popen(pingCmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
                with open("log.txt", "a") as log:
                    log.write(pingOutput)

                for line in pingOutput.stdout:
                    if line.find("avg") != -1:
                        splittedLine = line.split("/")
                        avg = splittedLine[4]
                        avgs.append(avg)
            
            iteration += 1
            print(avgs)        

    finally:
        run_steps(teardown, ignore_errors=True)
