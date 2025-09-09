# SocketTester
TCP/UDP socket testing between machines

# Help
    ./socket_tester.py -h

```
usage: socket_tester.py [-h] {list,server,client} ...

positional arguments:
  {list,server,client}

options:
  -h, --help            show this help message and exit
```
# Server
    ./socket_tester.py server -h

```
usage: socket_tester.py server [-h] [-I IP] [-P IP] [-m {tcp,udp}]

options:
  -h, --help            show this help message and exit
  -I, --source-ip-address IP
  -P, --source-port IP
  -m, --mode {tcp,udp}
```
# Client
    ./socket_tester.py client -h
```
usage: socket_tester.py client [-h] [-I IP] [-P PORT] -d IP or HOSTNAME -p PORT [-m {tcp,udp}]

options:
  -h, --help            show this help message and exit
  -I, --source-ip-address IP
  -P, --source-port PORT
  -d, --destination IP or HOSTNAME
  -p, --destination-port PORT
  -m, --mode {tcp,udp}
```
