import asyncio

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())
        self.message = input(">> ")
        self.transport.write(self.message.encode())

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('GAME OVER!')
        self.loop.stop()

loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda: ClientProtocol(loop),'127.0.0.1', 9999) #loopback address added
loop.run_until_complete(coro)
try:
    loop.run_forever()
except:
    pass

loop.close()
