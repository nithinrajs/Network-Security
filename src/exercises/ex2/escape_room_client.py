import socket
import time
quit = ""
client_socket = socket.socket()
port = 9090
client_socket.connect(('127.0.0.1',port))

try:
	output = client_socket.recv(4096)
	print(output.decode())
	while quit != "quit":
		data = input(">> ")
		quit = str(data)
		if quit != "quit":
			client_socket.send(data.encode())
			output = client_socket.recv(4096)
			print(output.decode())
		elif quit == "quit":
			client_socket.close()
			continue

except KeyboardInterrupt:
	client_socket.close()

finally:
	client_socket.close()
