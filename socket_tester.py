#!/usr/bin/env python3
import socket
from psutil import net_if_addrs
from argparse import ArgumentParser, Namespace

_socket_type = {
    'TCP': socket.SOCK_STREAM,
    'UDP': socket.SOCK_DGRAM
}


class CustomSocket:
    def __init__(self, mode: str, source_ip_address: str, source_port: int):
        self.s = socket.socket(socket.AF_INET, _socket_type.get(mode))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((source_ip_address, source_port))

    def print_source(self):
        print('Source IP: ', self.s.getsockname()[0])
        print('Source Port: ', self.s.getsockname()[1])


class TCPSocketServer(CustomSocket):
    def __init__(self, source_ip_address: str, source_port: int):
        super().__init__('TCP', source_ip_address, source_port)

    def listen(self):
        self.s.listen()

    def accept(self):
        return self.s.accept()


class TCPSocketClient(CustomSocket):
    def __init__(self, source_ip_address: str, source_port: int):
        super().__init__('TCP', source_ip_address, source_port)

    def connect(self, address):
        self.s.connect(address)

    def getpeername(self):
        return self.s.getpeername()


class UDPSocket(CustomSocket):
    def __init__(self, source_ip_address: str, source_port: int):
        super().__init__('UDP', source_ip_address, source_port)

    def sendto(self, data, address):
        self.s.sendto(data, address)

    def recvfrom(self):
        return self.s.recvfrom(1024)


class NetInterface:
    def __init__(self, name, ip, mask):
        self.name = name
        self.ip = ip
        self.mask = mask


class InterfaceInfo:
    def __init__(self):
        self.interfaces = []
        for interface, addrs in net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    self.interfaces.append(NetInterface(interface, addr.address, addr.netmask))


def separator(n: int = 20, c: str = '-'):
    print(c * n)


def list_interfaces(args):
    separator()
    interfaces = InterfaceInfo()
    for interface in interfaces.interfaces:
        print(f'Interface: {interface.name}')
        print(f'IP: {interface.ip}')
        print(f'Mask: {interface.mask}')
        separator()


def print_banner(mode: str):
    print(f'{mode} Socket Testing\n')


def print_destination(address):
    print('Destination IP: ', address[0])
    print('Destination Port: ', address[1])


def print_waiting():
    print('Waiting for connection...\n')


def print_info(s: CustomSocket, mode: str):
    print_banner(mode)
    s.print_source()
    print_waiting()


def server_run(args):
    if args.mode.upper() == 'TCP':
        s = TCPSocketServer(args.source_ip_address, args.source_port)
        s.listen()

        print_info(s, args.mode.upper())

        conn, addr = s.accept()
        print_destination(addr)
    else:
        s = UDPSocket(args.source_ip_address, args.source_port)

        print_info(s, args.mode.upper())

        data, addr = s.recvfrom()
        print_destination(addr)
        s.sendto(data, addr)


def client_run(args):
    if args.mode.upper() == 'TCP':
        s = TCPSocketClient(args.source_ip_address, args.source_port)

        print_info(s, args.mode.upper())

        s.connect((args.destination, args.destination_port))
        print_destination(s.getpeername())
    else:
        s = UDPSocket(args.source_ip_address, args.source_port)

        print_info(s, args.mode.upper())

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
        default=socket.gethostbyname(socket.gethostname())
    )
    server_parser.add_argument(
        '-P', '--source-port',
        type=int,
        metavar='IP',
        default=0
    )
    server_parser.add_argument(
        '-m', '--mode',
        choices=['tcp', 'udp'],
        default='tcp'
    )

    # PROGRAM client
    client_parser = subparsers.add_parser('client')
    client_parser.set_defaults(func=client_run)

    client_parser.add_argument(
        '-I', '--source-ip-address',
        metavar='IP',
        default=socket.gethostbyname(socket.gethostname())
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
        '-m', '--mode',
        choices=['tcp', 'udp'],
        default='tcp'
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
