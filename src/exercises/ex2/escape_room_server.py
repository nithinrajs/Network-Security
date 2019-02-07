import socket
from grading_escape_room import EscapeRoom
import time


server_socket = socket.socket()
port = 9090
server_socket.bind(('',port))
server_socket.listen(1)
conn, addr = server_socket.accept()
connected = "Welcome to Escape Room!\nYou are in a Escape Room now and you might want to start by 'look'ing around!\nInput 'quit' if you want to quit the game"
room = EscapeRoom()
room.start()

try:
	conn.send(connected.encode())
	while room.status() == "locked":
		data = conn.recv(4096)
		data1 = str(data.decode())
		output = room.command(data1.strip())
		conn.sendall(output.encode())

	if room.status() == "escaped":
		conn.send(b"Congratulations! You escaped!")
		conn.close()
	
	elif room.status() == "dead":
		conn.send(b"\n\nOh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly gas...")
		conn.close()
	
except KeyboardInterrupt:
	conn.close()

except BrokenPipeError:
	conn.close()

except ConnectionResetError:
	conn.close()

finally:
	conn.close()

