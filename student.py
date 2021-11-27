from tree_search import *
import math
import asyncio
import getpass
import json
import os
from piece import *

import websockets
import time


class Student(SearchDomain):
    def __init__(self):
        pass
    
    def result(self, actions, piece):
        #print("Actionsssssssss: " + actions)
        for action in actions:
            #print("Action:          " + action)      
            if action == 'a':
                piece.translate(-1,0)
            elif action == 'd':
                piece.translate(1,0)
            elif action == 'w': 
                if piece.plan == O:
                    pass
                else:
                    piece.rotate()
        return piece
        
                                     
    def satisfies(self, all_possibilities, stateGame):
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

            #print("ALL POSSIBILITIES (TEM QUE DAR SEMPRE :)")
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
            #print()
            #print("FUTURO E MAIS ALEM:      ", future_stateGame)
            #print()
            
            #future_stateGame = deepcopy( stateGame["game"] + positions_piece) 

            #print("JOgo de agr" + str(stateGame))
            #print("Peca de agr dps da acao", positions_piece)
            #print("Peça de agr dps da acao em baixo ", positions_piece_bottom)

            action_heuristic[piece_action[1]] = self.heuristic(future_stateGame)
            #print("Futuro jogo ", future_stateGame)
            #print("Heuristica da acao ", piece_action[1], " = ", action_heuristic[piece_action[1]])
        
        min_heuristic = -10000
        action_to_do = " "
        for key in action_heuristic:
            print("Action: " ,key, " , heuristica " , action_heuristic[key])
            if action_heuristic[key] > min_heuristic:
                min_heuristic = action_heuristic[key]
                action_to_do = key 

        print("AQUIIIII:        ", action_to_do, " HEURISTICA ", min_heuristic)
        
        return action_to_do

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
        heights = self.columns_height(state)
        holes = 0
        for i in range(8):
            for y in range(30 - heights[i], 30):
                if [i + 1, y] not in state:
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
        for x, y in state:
            if 30 - y > high_column[x - 1]:
                high_column[x - 1] = 30 - y
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
        next_pieces = []
        while True:
            try:
                state = json.loads(
                        await websocket.recv()
                    ) 
                if next_pieces != state.get("next_pieces"):
                    next_pieces = state.get("next_pieces")
                    # receive game update, this must be called timely or your game will get out of sync with the server

                    # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                    #print("STATE ", state)
                    if state.get("piece") != None:
                        piece = Piece(state.get("piece"))
                        p = SearchProblem(student,piece)
                        #print("PECA NO STUDENT QUE ESTA A CAIR ", piece.plan )
                        key = p.search(state)
                        #print("KEYYYY   : ", key)
                        for action in key:
                            await websocket.send(
                                json.dumps({"cmd": "key", "key": action})
                                
                            )  # send key command to server - you must implement this send in the AI agent
                            time.sleep(0.125)
                            

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