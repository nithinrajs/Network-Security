import asyncio
from grading_escape_room import EscapeRoom

class ServerProtocol(asyncio.Protocol):

	 def __init__(self):
	 	self.room = EscapeRoom()
	 	self.room.start()

	 def connection_made(self, transport):
	 	peername = transport.get_extra_info('peername')
	 	print('Connection from {}'.format(peername))
	 	self.transport = transport
	 	self.transport.write(b"Welcome to EscapeRoom!\nYou are in a Escape Room now and you might want to start by 'look'ing around!")

	 def data_received(self, data):
	 	message = str(data.decode())
	 	#print(message)
	 	#print('Data received: {!r}'.format(message))
	 	if self.room.status() == "locked":
	 		output = self.room.command(message.strip())
	 		self.transport.write(output.encode())
	 	if self.room.status() == "escaped":
	 		self.transport.write(b"Congratulations! You escaped!")
	 		self.transport.close()
	 	elif self.room.status() == "dead":
	 		self.transport.write(b"Oh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly gas...")
	 		self.transport.close()
	
def main():
	loop = asyncio.get_event_loop()
	bind = loop.create_server(ServerProtocol, '127.0.0.1', 9999)
	server = loop.run_until_complete(bind)
	
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()

if __name__ == "__main__":
	main()

