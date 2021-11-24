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
            piece.translate(-1,0)
            return piece
        elif action == 'd':
            piece.translate(1,0)
            return piece
        elif action == '':
            return piece
        elif action == 'w': 
            piece.rotate()
            return piece
        elif action == 's':
            piece.translate(0,1)
            return piece
        
                                     
    def satisfies(self, all_possibilities, stateGame):
        #print("JOgo de agr" + str(stateGame))
        action_heuristic = {}
        for piece_action in all_possibilities:
            piece = deepcopy(piece_action[0])

            abcissas_piece = []
            positions_piece = deepcopy([])
            for pos in piece.positions:
                positions_piece.append([deepcopy(pos)[0], deepcopy(pos)[1]])
                abcissas_piece.append(pos[0])

            miny_instateGame = 30
            if stateGame["game"] != []:
                for c in stateGame["game"]:
                    if miny_instateGame > c[1] and c[0] in abcissas_piece:
                        miny_instateGame = c[1]

            #print("ALL POSSIBILITIES (TEM QUE DAR SEMPRE =)")
            #for c in all_possibilities:
                #print(f"{c[0]}")
            #print("Deepcopy funciona fds, Peca de agr", positions_piece)

            positions_piece_bottom = deepcopy(positions_piece)
            flag = True
            while flag:

                for c in range(len(positions_piece)):
                    if positions_piece_bottom[c][1] + 1 >= miny_instateGame and positions_piece_bottom[c][0] in abcissas_piece:
                        flag = False

                if flag:
                    for c in range(len(positions_piece)):
                        val = positions_piece_bottom[c][1] + 1
                        positions_piece_bottom[c][1] = val

            future_stateGame = deepcopy( stateGame["game"] + deepcopy(positions_piece_bottom))
            #future_stateGame = deepcopy( stateGame["game"] + positions_piece) 

            #print("Peca de agr", positions_piece)
            #print("Peça agr em baixo ", positions_piece_bottom)

            action_heuristic[piece_action[1]] = self.heuristic(future_stateGame)
            #print("Futuro jogo ", future_stateGame)
        
        min_heuristic = ("a", action_heuristic["a"])
        for key in action_heuristic:
            #print("Action: " ,key, " , heuristica " , action_heuristic[key])
            if min_heuristic[1] < action_heuristic[key]:
                min_heuristic = (key, action_heuristic[key])


        return min_heuristic[0]

    def aggregate_height(self, state):
        high_column = self.columns_height(state)
        return sum(high_column)

    def bumpiness(self,state):
        bumpiness = 0
        high_column = self.columns_height(state)
        for i in range(len(high_column) - 1):
            bumpiness += abs(high_column[i] - high_column[i+1])
        return bumpiness

    def holes(self, state):
        holes = 0
        max_height = max(self.columns_height(state))
        y = 30 - max_height
        for coord in state:
                if (y + 1) < 30:
                    coord_below= [coord[0], y + 1]
                    y += 1
                    if coord_below not in state:
                        holes += 1
        return holes
    
    def completed_lines(self, state):
        highest = max(self.columns_height(state))
        completed = 0
        y = 30 - highest
        x = 1
        for _ in range(y * 8):     
            coord_tmp = [x , y]
            if coord_tmp in state:
                x += 1
            else:
                y += 1
                x = 1
            if x == 8:
                completed += 1
                x = 1
                y += 1
        return completed
    
    def columns_height(self, state):
        high_column = [0,0,0,0,0,0,0,0]
        for coord in state:
            if high_column[coord[0] - 1] < (30 - coord[1]):
                high_column[coord[0] - 1] =  30 - coord[1]
        return high_column

    # custo estimado de chegar de um estado a outro
    def heuristic(self, state):
        #return self.aggregate_height(state) + self.bumpiness(state) + self.holes(state) + self.completed_lines(state)
        return (self.aggregate_height(state) * -0.510066) + (self.bumpiness(state) * -0.184483) + (self.holes(state)* -0.35663) + (self.completed_lines(state) * 0.760666)
    
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        student = Student()
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                print("STATE ", state)
                if state.get("piece") != None:
                    piece = Piece(state.get("piece"))
                    p = SearchProblem(student,piece)
                 #   print("PECA NO STUDENT QUE ESTA A CAIR ", piece.plan )
                    key = p.search(state)
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



