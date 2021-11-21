#
# Module: cidades
# 
# Implements a SearchDomain for find paths between cities
# using the tree_search module
#
# (c) Luis Seabra Lopes
# Introducao a Inteligencia Artificial, 2012-2020
# Inteligência Artificial, 2014-2020
#


from tree_search import *
import math
import asyncio
import getpass
import json
import os

import websockets


class Student(SearchDomain):
    def __init__(self):
        pass
    
    def result(self, action, positions):
        
        if action == 'left':
            return self.translate(-1,0,positions) 
        elif action == 'right':
            pass
        elif action == 'down':
            pass
        elif action == 'drop':
            pass
        elif action == 'rotate': 
            pass
                                     
    def satisfies(self, positions):
        return True

    def translate(self, x, y, positions):
        x = int(x)
        y = int(y)
        positions = [ [cx + x , cy + y ] for cx, cy in positions]
        if all(-1 < pos[0] < 10 and -1 < pos[1] < 30 for pos in positions):
            return [ (cx + x , cy + y ) for cx, cy in positions]
        return []

    def cost(self, state, action):
        pass
    
    # custo estimado de chegar de um estado a outro
    def heuristic(self, state, goal):
        pass
    

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        variavel = True

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                print("OLAAAA ", state)

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                student = Student()
                p = SearchProblem(student,state.get("piece"))
                t = SearchTree(p,'depth')
                if variavel:
                    key = t.search()
                    variavel = False

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return




# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))



