
import socket
import threading

from icecream import ic

class Router:

    def __init__(self, name, ip, ports, neighbours):
        self.name = name
        self.ip = ip
        self.neighbours = neighbours
        self.port_tcp = ports[0]
        self.port_udp = ports[1]
        # create a thread for the tcp server
        udpServer = threading.Thread(target=self.startRouter)
        udpServer.start()
        # self.startRouter()

    def startRouter(self):
        # waiting for messages by udp
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind((self.ip, self.port_udp))
        while True:
            data, addr = udp.recvfrom(1024)
            data = data.decode()
            data = eval(data)
            ic(data)
            path = data[0]
            request = data[1]
            timestamp = data[2]

            path = path.append(self.ip)

            # join them all in a list
            data = [path, request, timestamp]

            for neighbour in self.neighbours:
                if neighbour not in path:
                    udp.sendto(str(data).encode(), (neighbour, self.port_udp))