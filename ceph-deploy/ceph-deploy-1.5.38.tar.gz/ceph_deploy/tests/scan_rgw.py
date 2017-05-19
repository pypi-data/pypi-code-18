import socket
from contextlib import closing

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.settimeout(2)  # 2 Second Timeout


def generate_ips(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))

    return ip_range

count = 0
for address in generate_ips('192.168.1.1', '192.168.1.255'):
    count += 1
    for port in [80, 7480]:
        print address, port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 Second Timeout

        result = sock.connect_ex((address, port))
        if result == 0:
            print 'port %s OPEN on %s' % (port, address)
        sock.close()

print 'Total scanned addresses: %s' % count
