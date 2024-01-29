import sys
import os
import socket

from tkinter import Tk

from Server import Server
from Client import Client
from Router import Router
from RP import Rp

def connectBootstraper(serverIp):
      # Connect to the bootstraper
      bootstraper = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      bootstraper.connect((serverIp, 5000))
      message = "connect"
      bootstraper.send(message.encode())
      # receive the neighbours
      dict = bootstraper.recv(1024).decode()
      # neighbours is a string, so we need to convert it to a dictionary
      left, right, rp_ip = dict.split(";")
      dict = eval(left)
      bootstraper.close()
      return {"Info": dict, "IP": right, "RP": rp_ip}

def main(args):
    # Go to BootStrapper get Info
    info = connectBootstraper(args[1])
    if info["Info"]["type"] == "server":
        server = Server(info["IP"], info["Info"]["neighbors"], info["RP"])
        server.main()
    elif info["Info"]["type"] == "client":
        os.environ.__setitem__('DISPLAY', ':0.0')	

        try:
            port = 5000
        except:
            print("[Usage: Cliente.py]\n")	
        root = Tk()

        client = Client(info["Info"]["neighbors"], info["IP"])
        client.master.title("Cliente Exemplo")	
        root.mainloop()
    elif info["Info"]["type"] == "router":
         if info["Info"]["Rp"]:
            rp = Rp(info["IP"], info["Info"]["neighbors"], [5000, 6000])
         else:
            router = Router(info["IP"], info["Info"]["neighbors"], [5000, 6000])
    else:
        print("Node doesn't belong to the network!!")

if __name__ == "__main__":
    main(sys.args)