import asyncio
import sys

stdin_queue = []


def get_user_data():
    line_in = sys.stdin.readline()
    line_in = line_in[:-1]
    stdin_queue.append(line_in)


async def async_input(prompt):
 print(prompt, end="")
 sys.stdout.flush()
 while len(stdin_queue) == 0:
    await asyncio.sleep(.1)
 return stdin_queue.pop(0)

async def game_runner(protocol):
        while True:
            command = await async_input(">> ")
            protocol.transport.write(command.encode())
            await asyncio.sleep(.1)  #Temporary
            

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
    
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())
        
        #self.message = get_user_data()


    def connection_lost(self, exc):
        print('The server closed the connection')
        print('GAME OVER!')
        self.loop.stop()


        # await a response... see if you can figure this part out!

loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda: ClientProtocol(loop),'', 9999)
transport, protocol = loop.run_until_complete(coro)
loop.add_reader(sys.stdin, get_user_data)
asyncio.ensure_future(game_runner(protocol))
loop.run_forever()
loop.close()
