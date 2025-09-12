[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/signalhackerpy)

# SocketTester
TCP/UDP socket testing between machines (IPv4 and IPv6 supported)

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
usage: socket_tester.py server [-h] [-I IP] [-P IP] [-s {tcp,udp}] [-t {4,6}]

options:
  -h, --help            show this help message and exit
  -I, --source-ip-address IP
  -P, --source-port IP
  -s, --socket-type {tcp,udp}
  -t, --family-type {4,6}
```
# Client
    ./socket_tester.py client -h
```
usage: socket_tester.py client [-h] [-I IP] [-P PORT] -d IP or HOSTNAME -p PORT [-s {tcp,udp}]
                               [-t {4,6}]

options:
  -h, --help            show this help message and exit
  -I, --source-ip-address IP
  -P, --source-port PORT
  -d, --destination IP or HOSTNAME
  -p, --destination-port PORT
  -s, --socket-type {tcp,udp}
  -t, --family-type {4,6}
```
