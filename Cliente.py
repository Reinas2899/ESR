import sys
import os
from tkinter import Tk
from ClienteGUI import ClienteGUI
os.environ.__setitem__('DISPLAY', ':0.0')	
if __name__ == "__main__":
	try:
		port = 5000
	except:
		print("[Usage: Cliente.py]\n")	
	
	root = Tk()

	serverIp = input("Digite o IP do servidor: ")
	
	# Create a new client
	app = ClienteGUI(root, port, serverIp)
	app.master.title("Cliente Exemplo")	
	root.mainloop()
	
