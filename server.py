import socket
import threading

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
server_socket.listen()

# list connected clients dan nickname mereka
clients = []
nicknames = []

# broadcast message ke connected client
def broadcast(message):
	for client in clients:
		client.send(message)


# function untuk terima message dari client lalu broadcast messagenya
# maksudnya, terima dari client A, lalu broadcast ke client lain
def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast(f'[Server] {nickname} left the chat.'.encode())
			nicknames.remove(nickname)
			break


def reviece():
	while True:
		client, address = server_socket.accept()
		print(f'[!] A client connected with {str(address)}')

		# tanya nickname dari client yang barusan connected
		client.send("WHO".encode()) # WHO ARE YOU?
		nickname = client.recv(1024).decode() # nickname user

		nicknames.append(nickname)
		clients.append(client)

		print(f'=> Nickname: {nickname}')
		broadcast(f'[Server] {nickname} has joined the chat!'.encode())
		client.send('[Server] you are connected to server! Happy chatting.'.encode()) # feedback kalo user udah connected ke server

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

reviece()
