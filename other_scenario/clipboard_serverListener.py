import socket
import keyboard
from time import sleep
from threading import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = ""
host_port = 0

print("[~] Getting local IP Address...")
host_ip = socket.gethostbyname(socket.gethostname())
print("[!] New IP : {}.".format(host_ip))
host_port = int(input("[?] Enter server listening port (default: 6969): ") or "6969")

print("[!] OK Starting Server, listening on:")
print("=> Host IP:\t", host_ip)
print("=> Port:\t\t", host_port)

server_socket.bind((host_ip, host_port))

class client(Thread):
	def __init__(self, socket, address):
		Thread.__init__(self)
		self.sock = socket
		self.addr = address
		self.start()

	def run(self):
		while True:
			try:
				client_message = self.sock.recv(1024).decode()
				
				if len(client_message) > 5:
					if(client_message == "imdone" or client_message == "exit()"):
						self.sock.send(b"Server : Goodbye...")
						self.sock.close()
						break
					else:
						keyboard.send("ctrl+f")
						sleep(.2)
						keyboard.write(client_message)
						sleep(.2)
						keyboard.send("enter")

					self.sock.send(b"Server : Job complete!")
				else:
					self.sock.send(b"Server : Text you copied is to short!")
				
			except Exception as e:
				print(e)
				self.sock.close()
				print("[!] Error Occured. Closing Server...")
				break

server_socket.listen(5)
print("Server started!")
while True:
	clientsocket, address = server_socket.accept()
	client(clientsocket, address)
	break

