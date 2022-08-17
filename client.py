import socket
from time import sleep

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = ""
server_port = 0

print("[!] Enter server details.")
server_ip = input("Server IP Address : ")
server_port = int(input("Port: "))

print("[~] Connecting to {}...".format(server_ip))

try:
	client_socket.connect((server_ip, server_port))
except Exception as e:
	print(e)
	print("[!] Error connecting to server {} on port {}, check if server running or not.".format(server_ip, server_port))
	exit()
else:
	print("[!] Connected to {} on port {}.".format(server_ip, server_port))

def send(message: str):
	client_socket.send(message.encode())
	recieved_data_from_server = client_socket.recv(1024).decode()
	print(recieved_data_from_server)

def main():
	while True:
		try:
			input_message = input('Enter Message : ')
			if input_message=="exit()" or  input_message=="bye()":
				send(str(input_message))
				print("[!] Closing...")
				sleep(3)
				break
			else:
				send(str(input_message))
		except Exception as e:
			print(e)
			client_socket.close()
			break

if __name__ == "__main__":
	print("Type 'exit()' or 'bye()' to end the session.")
	main()