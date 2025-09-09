#!/usr/bin/env python3
import socket
from psutil import net_if_addrs
from argparse import ArgumentParser, Namespace

_family_type = {
    4: socket.AF_INET,
    6: socket.AF_INET6
}
_socket_type = {
    'TCP': socket.SOCK_STREAM,
    'UDP': socket.SOCK_DGRAM
}


class CustomSocket:
    def __init__(self, family_type: int, socket_type: str, addr):
        self.s = socket.socket(_family_type.get(family_type), _socket_type.get(socket_type.upper()))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(addr)

    def print_source(self):
        print('Source IP: ', self.s.getsockname()[0])
        print('Source Port: ', self.s.getsockname()[1])


class TCPSocketServer(CustomSocket):
    def __init__(self, family_type: int, addr):
        super().__init__(family_type, 'TCP', addr)

    def listen(self):
        self.s.listen()

    def accept(self):
        return self.s.accept()


class TCPSocketClient(CustomSocket):
    def __init__(self, family_type: int, addr):
        super().__init__(family_type, 'TCP', addr)

    def connect(self, address):
        self.s.connect(address)

    def getpeername(self):
        return self.s.getpeername()


class UDPSocket(CustomSocket):
    def __init__(self, family_type: int, addr):
        super().__init__(family_type, 'UDP', addr)

    def sendto(self, data, address):
        self.s.sendto(data, address)

    def recvfrom(self):
        return self.s.recvfrom(1024)


class NetInterface:
    def __init__(self, name, ip, mask, af):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.af = af


class InterfaceInfo:
    def __init__(self):
        self.interfaces = []
        for interface, addrs in net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET or addr.family == socket.AF_INET6:
                    self.interfaces.append(NetInterface(interface, addr.address, addr.netmask, addr.family))


def separator(n: int = 50, c: str = '-'):
    print(c * n)


def list_interfaces(args):
    separator()
    interfaces = InterfaceInfo()
    for interface in interfaces.interfaces:
        print(f'Interface: {interface.name}')
        print(f'IP: {interface.ip}')
        print(f'Mask: {interface.mask}')
        separator()


def get_source_ip_info(socket_type: str, family_type: int, source_ip_address: str, source_port: int):
    if not source_ip_address:
        interfaces = InterfaceInfo()
        int_ip = ''
        for interface in interfaces.interfaces:
            if not interface.name.startswith('lo') and (interface.af == _family_type.get(family_type)):
                int_ip = interface.ip
                break
        return socket.getaddrinfo(int_ip, source_port, _family_type.get(family_type),
                                  _socket_type.get(socket_type))[0][4]

    return socket.getaddrinfo(source_ip_address, source_port, _family_type.get(family_type),
                              _socket_type.get(socket_type))[0][4]


def print_banner(socket_type: str):
    print(f'{socket_type} Socket Testing\n')


def print_destination(address):
    print('Destination IP: ', address[0])
    print('Destination Port: ', address[1])


def print_waiting():
    print('Waiting for connection...\n')


def print_info(s: CustomSocket, socket_type: str):
    print_banner(socket_type)
    s.print_source()
    print_waiting()


def server_run(args):
    args.source_addr = get_source_ip_info(args.socket_type.upper(), args.family_type, args.source_ip_address,
                                          args.source_port)
    if args.socket_type.upper() == 'TCP':
        s = TCPSocketServer(args.family_type, args.source_addr)
        s.listen()

        print_info(s, args.socket_type.upper())

        conn, addr = s.accept()
        print_destination(addr)
    else:
        s = UDPSocket(args.family_type, args.source_addr)

        print_info(s, args.socket_type.upper())

        data, addr = s.recvfrom()
        print_destination(addr)
        s.sendto(data, addr)


def client_run(args):
    args.source_addr = get_source_ip_info(args.socket_type.upper(), args.family_type, args.source_ip_address,
                                          args.source_port)
    if args.socket_type.upper() == 'TCP':
        s = TCPSocketClient(args.family_type, args.source_addr)

        print_info(s, args.socket_type.upper())

        s.connect((args.destination, args.destination_port))
        print_destination(s.getpeername())
    else:
        s = UDPSocket(args.family_type, args.source_addr)

        print_info(s, args.socket_type.upper())

        s.sendto(b'0', (args.destination, args.destination_port))
        data, addr = s.recvfrom()
        print_destination(addr)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    # PROGRAM list
    list_interface_parser = subparsers.add_parser('list')
    list_interface_parser.set_defaults(func=list_interfaces)

    # PROGRAM server
    server_parser = subparsers.add_parser('server')
    server_parser.set_defaults(func=server_run)

    server_parser.add_argument(
        '-I', '--source-ip-address',
        metavar='IP',
    )
    server_parser.add_argument(
        '-P', '--source-port',
        type=int,
        metavar='IP',
        default=0
    )
    server_parser.add_argument(
        '-s', '--socket-type',
        choices=['tcp', 'udp'],
        default='tcp'
    )
    server_parser.add_argument(
        '-t', '--family-type',
        choices=[4, 6],
        default=4,
        type=int,
    )

    # PROGRAM client
    client_parser = subparsers.add_parser('client')
    client_parser.set_defaults(func=client_run)

    client_parser.add_argument(
        '-I', '--source-ip-address',
        metavar='IP',
    )
    client_parser.add_argument(
        '-P', '--source-port',
        type=int,
        metavar='PORT',
        default=0
    )
    client_parser.add_argument(
        '-d', '--destination',
        metavar='IP or HOSTNAME',
        required=True
    )
    client_parser.add_argument(
        '-p', '--destination-port',
        type=int,
        metavar='PORT',
        required=True
    )
    client_parser.add_argument(
        '-s', '--socket-type',
        choices=['tcp', 'udp'],
        default='tcp'
    )
    client_parser.add_argument(
        '-t', '--family-type',
        type=int,
        choices=[4, 6],
        default=4
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        print('Check the help with -h')


if __name__ == '__main__':
    main()
