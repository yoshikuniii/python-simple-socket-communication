import socket
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
				if client_message == "exit()" or client_message == "bye()":
					print("End Session. Exiting...")
					self.sock.send(b"Server : Goodbye...")
					self.sock.close()
					break
				else:
					print("Client {} say : {}".format(self.addr, client_message))
					self.sock.send(b"Server : Message Recieved!") # tell client that the message has been recieved
				
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

