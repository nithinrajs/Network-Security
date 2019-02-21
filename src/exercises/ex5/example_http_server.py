import asyncio
import sys
import re
import os
from datetime import datetime

class ExampleHttpServer(asyncio.Protocol):
	def __init__(self, document_root):
		self.document_root = document_root
		self.request = {}
		self.request_header = []
		self.buffer = b""
		self.size = 0
		self.error = "<html><body><h1>404 Not Found</h1></body></html>"
		self.date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
		self.modify_date = ""
		self.response = {
			"Date" : self.date,
			"Server" : "NetSec Prototype Server 1.0",
			"Last-Modified" : "",
			"Content-Length" : "",
			"Connection" : "close",
			"Content-Type" : "text/html"
		}

		self.response_fail = {
			"Date" : self.date,
			"Server" : "NetSec Prototype Server 1.0",
			"Content-Length" : 50,
		}

	def connection_made(self,transport):
		self.transport = transport

	def data_received(self,data):
		self.buffer += data
		if not self.has_full_packet(self.buffer):
			return
		self.request = self.buffer.decode()
		self.request = self.request.split("\n")
		self.request_header = self.request[0].split(" ")
		print(*self.request[1:-2], sep="\n")
		print(self.request_header)
		if self.request_header[0] == "GET" and self.request_header[2] == "HTTP/1.1\r":
			filename = self.document_root + self.request_header[1]
			uri = filename.split('/')
			directory = '/'.join(uri[:-1])
			#print(filename)
			#print(directory)
			if os.path.isfile(filename):
				self.size = os.path.getsize(filename)
				modify = os.stat(filename)
				self.modify_date = datetime.fromtimestamp(modify.st_mtime).strftime("%a, %d %b %Y %H:%M:%S GMT")  # Last modified time
				self.response['Last-Modified'] = self.modify_date
				self.response['Content-Length'] = self.size
				file = open(filename, 'r')
				body = file.read()
				self.transport.write(b"HTTP/1.1 200 OK")
				self.transport.write(b"\n")
				response = ''.join('%s: %s\n' % (key, value) for key, value in self.response.items())
				self.transport.write(response.encode())
				self.transport.write(b"\n")
				self.transport.write(body.encode())
				self.transport.close()

			elif os.path.isfile(directory + "/index.html"):  #get default index.html if exists in the directory instead of 404
				default = directory+"/index.html"
				self.size = os.path.getsize(default)
				modify = os.stat(default)
				self.modify_date = datetime.fromtimestamp(modify.st_mtime).strftime("%a, %d %b %Y %H:%M:%S GMT")  # Last modified time
				self.response['Last-Modified'] = self.modify_date
				self.response['Content-Length'] = self.size
				file = open(default, 'r')
				body = file.read()
				self.transport.write(b"HTTP/1.1 200 OK")
				self.transport.write(b"\n")
				response = ''.join('%s: %s\n' % (key, value) for key, value in self.response.items())
				self.transport.write(response.encode())
				self.transport.write(b"\n")
				self.transport.write(body.encode())
				self.transport.close()

			else:
				self.transport.write(b"HTTP/1.1 404 Not Found")
				self.transport.write(b"\n")
				response = ''.join('%s: %s\n' % (key, value) for key, value in self.response_fail.items())
				self.transport.write(response.encode())
				self.transport.write(b"\n")
				self.transport.write(self.error.encode())
				self.transport.close()
				
		else:
			self.transport.write(b"HTTP/1.1 404 Not Found")
			self.transport.write(b"\n")
			response = ''.join('%s: %s\n' % (key, value) for key, value in self.response_fail.items())
			self.transport.write(response.encode())
			self.transport.write(b"\n")
			self.transport.write(self.error.encode())
			self.transport.close()
			
	def has_full_packet(self, buffer):
		match = re.search(rb'(\r\n){2}',buffer,re.M)
		if match:
			return True
		else:
			return False

def main():
	document_root = sys.argv[1] # first command line parameter
	loop = asyncio.get_event_loop()
	bind = loop.create_server(lambda: ExampleHttpServer(document_root), '127.0.0.1', 8080)
	server = loop.run_until_complete(bind)
	print('SERVER RUNNING ON: {}'.format(server.sockets[0].getsockname()))
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()

if __name__ == "__main__":
	main()
