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
        elif action == '':
            return piece
        elif action == 'w': 
            piece.shape.rotate()
            return piece
        
                                     
    def satisfies(self, all_possibilities, stateGame):
        action_heuristic = {}
        for piece_action in all_possibilities:
            piece = piece_action[0]
            positions_piece = []
            for pos in piece.shape.positions:
                positions_piece.append([pos[0], pos[1]])

            future_stateGame = stateGame["game"] + positions_piece

            action_heuristic[piece_action[1]] = self.heuristic(future_stateGame)
            #print("Futuro jogo ", future_stateGame)
        
        min_heuristic = ("a", action_heuristic["a"])
        for key in action_heuristic:
            print("Action: " ,key, " , heuristica " , action_heuristic[key])
            if min_heuristic[1] > action_heuristic[key]:
                min_heuristic = (key, action_heuristic[key])


        return min_heuristic[0]

    def aggregate_height(self, state):
        high_column = [0,0,0,0,0,0,0,0]
        for coord in state:
            if high_column[coord[0] - 1] < (30 - coord[1]):
                high_column[coord[0] - 1] =  30 - coord[1]
        #print("Coluninhas ", high_column)
        return sum(high_column)

    def bumpiness(self, state):
        high_column = [0,0,0,0,0,0,0,0]
        for coord in state:
            if high_column[coord[0] - 1] < (30 - coord[1]):
                high_column[coord[0] - 1] =  30 - coord[1]
        bumpinessssss = 0
        for i in range(len(high_column) - 1):
            bumpinessssss += abs(high_column[i] - high_column[i+1])
        return bumpinessssss
    
    def holes(self, state):
        high_column = [0,0,0,0,0,0,0,0]
        for coord in state:
            if high_column[coord[0] - 1] < (30 - coord[1]):
                high_column[coord[0] - 1] =  30 - coord[1]
        
        hole = 0
        for max_column in high_column:
            idx = 30 - max_column
            i = 1
            for coord in state:
                if coord[0] == i:
                    lista = [i, idx]
                    idx += 1
                    if lista not in state:
                        hole += 1
            i += 1
        
        return hole
    
    def completed_lines(self, state):
        high_column = [0,0,0,0,0,0,0,0]
        completed = 0
        for coord in state:
            if high_column[coord[0] - 1] < (30 - coord[1]):
                high_column[coord[0] - 1] =  30 - coord[1]
        
        highest = max(high_column)

        for coord in state:
            idx = 30 - highest
            i = 1
            lista = [i , idx]
            if lista in state:
                i += 1
            else:
                idx +=1
                i = 1
            
            if i == 8:
                completed += 1 
        return completed
            
    def cost(self, state, action):
        pass
    
    # custo estimado de chegar de um estado a outro
    def heuristic(self, state):
        #return self.aggregate_height(state) + self.bumpiness(state) + self.holes(state) + self.completed_lines(state)
        return (self.aggregate_height(state) * -0.510066) + (self.bumpiness(state) * -0.184483) + (self.holes(state)* -0.35663) + (self.completed_lines(state) * 0.760666)
    

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



