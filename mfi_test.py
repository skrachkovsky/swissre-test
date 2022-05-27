import re
import time

_ips = {}
_max_n = 0
_max_ip = ''
_rep = re.compile(r'\s+')
_start = time.time()
with open('./input/access10x.log', 'r') as file:
    for line in file:
        if not line.strip():
            continue
        cols = _rep.split(line)
        ip = cols[2]
        if ip not in _ips:
            _ips[ip] = 1
        else:
            _ips[ip] += 1
        if ip == _max_ip:
            _max_n = _ips[ip]
        elif _ips[ip] > _max_n:
            _max_n = _ips[ip]
            _max_ip = ip
    print(_max_ip)
    print(_max_n)
    print(time.time() - _start)
