import argparse
import asyncio
import time
from json import loads

import websockets

from Agent import Agent
from modulo import power_mod

SEND_STRING = "{}&{}&{}"

n = '3700996710331415883761755817563609804244919955' \
    '80600109524304692636792296120563363822977313410' \
    '19201644498600485976491104314754696444189169777' \
    '52674690008136691876722020817653675884503794620' \
    '43354336198833248696996620972969'

n = int(n)
e = 22953686867719691230002707821868552601124472329079


class WebSocketClient:
    uri = "ws://localhost:8763"
    client_name = ""

    def __init__(self, client_name, uri, password):
        self.client_name = client_name
        self.uri = uri
        self.password = power_mod(password, e, n)
        self.state = None
        self.agent = Agent()

    async def start_testing(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    await websocket.send(SEND_STRING.format(self.client_name, "-1", self.password))
                    self.state = await websocket.recv()
                    self.state = loads(self.state)
                    print(self.state)
                    while isinstance(self.state, list) or \
                            (
                                    isinstance(self.state, str)
                                    and not self.state.startswith('END')
                            ):
                        action = self.agent.select_action(self.state)
                        await websocket.send(SEND_STRING.format(self.client_name, action, "verified"))
                        self.state = await websocket.recv()
                        self.state = loads(self.state)
                        print(f'a:{action}, ns:"{self.state}')
                        while isinstance(self.state, str) and self.state.startswith("Error"):
                            # TODO: sleep some time
                            await websocket.send(SEND_STRING.format(self.client_name, action, "verified"))
                            self.state = await websocket.recv()
                break
            except:
                print("Some error occurred! Retrying in 5 seconds")
                time.sleep(5)
                continue


parser = argparse.ArgumentParser()
parser.add_argument('--client_name', type=str, required=True)
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--password', type=int, required=True)
args = parser.parse_args()
client = WebSocketClient(args.client_name, args.host, args.password)
asyncio.get_event_loop().run_until_complete(client.start_testing())
