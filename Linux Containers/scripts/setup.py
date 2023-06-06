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
    'ip netns exec NetNsB ip route add default via 192.168.2.1 dev eth0',
    'ip netns exec NetNsB /usr/sbin/sshd -o PidFile=/run/sshd-NetNsB.pid'
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

    except:
        print("An exception occured.!")
