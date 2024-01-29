from icecream import ic
import os
import sys
import socket
import threading
import json

def read_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Strip trailing newline characters from each line and create a list of strings
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data
    
'''def create_dict(data):
    config_dict = {}
    for key, value in data.items():
        config_dict

        config_dict["Rp"] = list(data.values())[0]
        config_dict["neighbors"] = list(data.values())[1]
        config_dict["type"] = list(data.values())[2]
        config_dict["port_tcp"] = 5000
        config_dict["port_udp"] = 6000
    return config_dict
    # create a dict from the json file'''

def sendNeighbours(dic, client_ip):
    for key, value in dic.items():
        if key == client_ip:
            # make the value a string
            value = str(value)
            # remove the square brackets
            value = value.replace("[", "")
            value = value.replace("]", "")
            # remove the single quotes
            value = value.replace("'", "")
            return value

def handle_client(client_socket, dicionario):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        vizinhos = sendNeighbours(dicionario, client_socket.getpeername()[0])
        client_socket.send(vizinhos.encode())
    client_socket.close()

def connectToClient(dic, rp_ip):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.0.4.1", 5000))
    server.listen(5)
    print("Server listening on port 5000")

    while True:
        client_socket, addr = server.accept()
        message = client_socket.recv(1024).decode()
        if message == "connect":
            # dic["ip"] = 
            ic(addr[0])
            message = str(dic[addr[0]]) + ";" + addr[0] + f";{rp_ip}" if dic[addr[0]][2] == "server" else ""
            ic(message)
            client_socket.send(message.encode())
        elif message == "get_servers":
            servers = getAllServers(dic)
            ic(servers)
            client_socket.send(str(servers).encode())
        else:
            pass
        '''message = client_socket.recv(1024).decode()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, dic))
        client_handler.start()'''

def getAllServers(dic):
    servers = []
    for key, value in dic.items():
        if value['type'] == "server":
            servers.append(key)
    return servers


def getRpIp(dic):
    for key, value in dic.items():
        if value['Rp'] == True:
            return key


def main():
    file_path = "config_file.json"
    data = read_json_file(file_path)
    rp_ip = getRpIp(data)
    # dicionario = create_dict(data)
    ic(data)
    connectToClient(data, rp_ip)


if __name__ == "__main__":
    main()
