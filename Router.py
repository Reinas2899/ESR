import socket
import threading
import json
import sys
from ServerWorker import ServerWorker
from ClienteGUI import ClienteGUI
from icecream import ic
from time import time

class Router:
    def __init__(self, name, ports):
        self.name = name
        self.ip = None
        self.isRp = False
        self.type = None
        self.neighbours = None
        self.port_tcp = ports[0]
        self.port_udp = ports[1]
        _ = ClienteGUI.connectBootstraper(self)
        if not self.isRp:
            # create a thread for the tcp server
            udpServer = threading.Thread(target=self.startRouter)
            udpServer.start()
            # self.startRouter()
        else:
            udpServer = threading.Thread(target=self.startRp)
            udpServer.start()

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
    
    def startRp(self):
        routingTable = {}
        serverTable = {}
        # create a tcp connextion using the port 5000 with threads per connection
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind((self.ip, self.port_tcp))
        threading.Thread(target=self.handleServers, agrs=(tcp, serverTable)).start()
        '''bootstraper = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bootstraper.connect(("10.0.4.1", 5000))
        message = "get_servers"
        bootstraper.send(message.encode())
        servers = bootstraper.recv(1024).decode()
        servers = eval(servers)
        for server in servers:
            serverTable[server[0]] = [0, "asleep"] # [latency, status]'''
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

            # add the path to the routing table
            if path[0] not in routingTable:
                routingTable[path[0]] = [path]
            else:
                routingTable[path[0]].append(path)

            if request == "start":
                anyActive = 0
                chosenServer = None
                for server in serverTable:
                    if serverTable[server][1] == "active":
                        anyActive = 1
                        chosenServer = server
                        break
                if anyActive == 0:
                    # choose the server with the lowest latency
                    lowestLatency = sys.maxsize()
                    chosenServer = None
                    for server in serverTable:
                        if serverTable[server][0] < lowestLatency:
                            lowestLatency = serverTable[server][0]
                            chosenServer = server
                    # send the request to the chosen server
                    #TO:DO
                udp.sendto(str(data).encode(), (chosenServer, self.port_udp))
    
    def handleServers(self, tcp, serverTable):
        while True:
            client_socket, addr = tcp.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=self.handleServerPackets, args=(client_socket, addr, serverTable))
            client_handler.start()

    def handleServerPackets(self, client_socket, addr, serverTable):
        # wait for packet
        data = client_socket.recv(1024).decode()
        timestamp = time()*1000
        serverTable[addr[0]] = [timestamp - data[0], "active"] # [latency, status]

if __name__ == "__main__":
    router = Router("R1", [5000, 6000])
    # Create a new client
    # app = ClienteGUI(root, addr, port)
    # app.master.title("Cliente Exemplo")	
    # root.mainloop()
    