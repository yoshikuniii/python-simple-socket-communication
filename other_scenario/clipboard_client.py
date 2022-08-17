import socket
import keyboard
import win32clipboard as clipboard
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
	cur_clip = ""
	new_clip = ""

	# get current clipboard
	clipboard.OpenClipboard()
	cur_clip = clipboard.GetClipboardData()
	clipboard.CloseClipboard()

	while True:
		keyboard.wait("ctrl+c")

		sleep(.1) # add delay to update copied text on clipboard
		clipboard.OpenClipboard()
		new_clip = clipboard.GetClipboardData()
		clipboard.CloseClipboard()

		if new_clip == cur_clip:
			print("You => Same text copied!")
			send(new_clip)
		elif(new_clip == "imdone"):
			send(new_clip)
			print("[!] Connection closed.")
			sleep(3)
			break
		else:
			print("You => New text copied!")
			cur_clip = new_clip # update current clipboard to newest clipboard
			send(cur_clip)

if __name__ == "__main__":
	main()
	exit()