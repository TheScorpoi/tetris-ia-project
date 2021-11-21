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
from piece import *

import websockets


class Student(SearchDomain):
    def __init__(self):
        pass
    
    def result(self, action, piece):
        
        if action == 'a':
            piece.shape.translate(-1,0)
            return piece
        elif action == 'd':
            piece.shape.translate(1,0)
            return piece
        elif action == 's':
            pass
        elif action == 'w': 
            piece.shape.rotate()
            return piece
        
                                     
    def satisfies(self, piece):
        return False
        pass

    def cost(self, state, action):
        pass
    
    # custo estimado de chegar de um estado a outro
    def heuristic(self, state, goal):
        pass
    

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                student = Student()
                piece = Piece(state.get("piece"))
                p = SearchProblem(student,piece)
                t = SearchTree(p,'depth')
                key = t.search(state)
                key = ""
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



