import socket
import threading
from os import system

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = ""
server_port = 0

# Input detail server
print("[!] Enter server details.")
server_ip = input("Server IP Address : ")
server_port = int(input("Port: "))

print("[~] Connecting to {}...".format(server_ip))

# Connect ke server
try:
	client_socket.connect((server_ip, server_port))
except Exception as e:
	print(e)
	print("[!] Error connecting to server {} on port {}, check if server running or not.".format(server_ip, server_port))
	exit()
else:
	print("[!] Connected to {} on port {}.".format(server_ip, server_port))


# user memasukan nickname
nickname = input("Choose your nickname: ")

stop_thread = False

def recieve():
	while True:
		global stop_thread
		if stop_thread:
			break
		try:
			# terima pesan
			message = client_socket.recv(1024).decode()
			
			# server menanyakan nickname user
			# ini hanya dilakukan sekali saat baru konek
			if message == "WHO": 
				client_socket.send(nickname.encode())
			else:
				print(message)
		except:
			client_socket.close()
			system('cls') # clear the error message hehe
			break

def send():
	while True:
		global stop_thread
		if stop_thread:
			break

		# tulis message baru
		message = f'{nickname}: {input("")}'

		if message[len(nickname)+2:].startswith('/bye'):
			# client_socket.send(f"[!] Client {nickname} disconnected!".encode())
			client_socket.close()
			system('cls')
			stop_thread = True


		client_socket.send(message.encode())

print("[!] Type '/bye' to end the session.")

recieve_thread = threading.Thread(target=recieve)
send_thread = threading.Thread(target=send)
recieve_thread.start()
send_thread.start()