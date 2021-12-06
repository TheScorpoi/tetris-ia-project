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
                #print("Peca sem rodar ", piece ) 
                if piece.plan == O:
                    pass
                else:
                    piece.rotate()
                #print("Peca dps de rodar ", piece ) 
        return piece
        
    def satisfies(self, all_possibilities, stateGame):
        action_heuristic = {}
        for piece_action in all_possibilities:
            piece = piece_action[0]

            positions_piece = []
            for pos in piece.positions:
                positions_piece.append([pos[0], pos[1]])


            #print("JOgo de agr" + str(stateGame))

            miny_instateGame = [30, 30, 30, 30, 30, 30, 30, 30]           #verificar 29 e 30!!!
            if stateGame["game"] != []:
                for c in stateGame["game"]:
                    if miny_instateGame[c[0] - 1] > c[1]:
                        miny_instateGame[c[0] - 1] = c[1]

            #print("MInimos y por cada coluna ", miny_instateGame)
            #print("ALL POSSIBILITIES (TEM QUE DAR SEMPRE :)")
            #for c in all_possibilities:
                #print(f"{c[0]}")
            #print("Deepcopy funciona fds, Peca de agr", positions_piece)

            #print("Peca de agr dps da acao", positions_piece)
            positions_piece_bottom = positions_piece
            flag = True
            while flag:

                for c in range(len(positions_piece)):
                    if positions_piece_bottom[c][1] + 1 >= miny_instateGame[positions_piece_bottom[c][0] - 1]:
                        flag = False

                if flag:
                    for c in range(len(positions_piece)):
                        val = positions_piece_bottom[c][1] + 1
                        positions_piece_bottom[c][1] = val

            future_stateGame = stateGame["game"] + positions_piece_bottom

            proximas_pecas = stateGame['next_pieces']
            if len(proximas_pecas) == 3:
                new_game = {}
                new_game['game'] = future_stateGame
                new_game['next_pieces'] = stateGame['next_pieces'][1:]    
  
                all_pos = []    
                peçaOriginal = deepcopy(self.get_piece_by_shape(proximas_pecas[0]))
                new_game['piece'] = peçaOriginal.positions
                for action in self.get_actions_by_shape(peçaOriginal):
                    new_piece = self.result(action, peçaOriginal)
                    all_pos.append((new_piece, action))
                    peçaOriginal = deepcopy(self.get_piece_by_shape(proximas_pecas[0]))
                #print("Todas as possibilidades", all_pos)
                #print("ALL POSSIBILITIES ")
                for c in all_pos:
                    print(f"{c[0]}   , action : {c[1]}")
                #print("NOvo jogo", new_game)
                action = self.satisfies(all_pos, new_game)

                '''

                new_game['game'] = new_game['game'] + [c[0].positions for c in all_pos if c[1] == action][0]
                new_game['next_pieces'] = stateGame['next_pieces'][2:]

                all_pos = []    
                peçaOriginal = deepcopy(self.get_piece_by_shape(proximas_pecas[1]))
                new_game['piece'] = peçaOriginal.positions
                for action in self.get_actions_by_shape(peçaOriginal):
                    new_piece = self.result(action, peçaOriginal)
                    all_pos.append((new_piece, action))
                    peçaOriginal = deepcopy(peçaOriginal)
                action = self.satisfies(all_pos, new_game)

                new_game.put['game'] = new_game['game'] + [c[0].positions for c in all_pos if c[1] == action][0]
                new_game.put['next_pieces'] = stateGame['next_pieces'][3:]
  
                all_pos = []    
                peçaOriginal = deepcopy(self.get_piece_by_shape(proximas_pecas[2]))
                new_game['piece'] = peçaOriginal.positions
                for action in self.get_actions_by_shape(peçaOriginal):
                    new_piece = self.result(action, peçaOriginal)
                    all_pos.append((new_piece, action))
                    peçaOriginal = deepcopy(peçaOriginal)
                action = self.satisfies(all_pos, new_game)
                '''
                resultado = self.result(action,peçaOriginal).positions

                positions_result = []
                for pos in resultado:
                    positions_result.append([pos[0], pos[1]])


                #print("JOgo de agr" + str(stateGame))

                miny_instateGame2 = [30, 30, 30, 30, 30, 30, 30, 30]           #verificar 29 e 30!!!
                if new_game['game'] != []:
                    for c in new_game['game']:
                        if miny_instateGame2[c[0] - 1] > c[1]:
                            miny_instateGame2[c[0] - 1] = c[1]

                #print("MInimos y por cada coluna ", miny_instateGame)
                #print("ALL POSSIBILITIES (TEM QUE DAR SEMPRE :)")
                #for c in all_possibilities:
                    #print(f"{c[0]}")
                #print("Deepcopy funciona fds, Peca de agr", positions_piece)

                #print("Peca de agr dps da acao", positions_piece)
                positions_result_bottom = positions_result
                flag = True
                while flag:

                    for c in range(len(positions_result)):
                        if positions_result_bottom[c][1] + 1 >= miny_instateGame2[positions_result_bottom[c][0] - 1]:
                            flag = False

                    if flag:
                        for c in range(len(positions_result)):
                            val = positions_result_bottom[c][1] + 1
                            positions_result_bottom[c][1] = val

                print("PRIMEIRA PECA - Estado do jogo com as duas peças la em baixo, acao da primeira peça:",piece_action[1] ,", estado:", new_game['game'] + positions_result_bottom)
                action_heuristic[piece_action[1]] = self.heuristic(new_game['game'] + positions_result_bottom)
                print("Heuristica ", action_heuristic[piece_action[1]] )
            else:
                print("SEGUNDA PECA - Estado do jogo com as duas peças la em baixo, acao da segunda peça:",piece_action[1] ,", estado:", future_stateGame)
                action_heuristic[piece_action[1]] = self.heuristic(future_stateGame)
                print("Heuristica ", action_heuristic[piece_action[1]] )


            #print()
            #print("FUTURO E MAIS ALEM:      ", future_stateGame)
            #print()
            
            #print("Acao que estamos a anlisar" , piece_action[1])
            #future_stateGame = deepcopy( stateGame["game"] + positions_piece) 

            #print("Peça de agr dps da acao em baixo ", positions_piece_bottom)

            #action_heuristic[piece_action[1]] = self.heuristic(future_stateGame)
            #print("Futuro jogo ", future_stateGame)
            #print("Heuristica da acao ", piece_action[1], " = ", action_heuristic[piece_action[1]])
        
        min_heuristic = -10000
        action_to_do = " "
        for key in action_heuristic:
            #print("Action: " ,key, " , heuristica " , action_heuristic[key])
            if action_heuristic[key] > min_heuristic:
                min_heuristic = action_heuristic[key]
                action_to_do = key 

        #print("AQUIIIII:        ", action_to_do, " HEURISTICA ", min_heuristic)
        
        return action_to_do

    def get_actions_by_shape(self, piece):
        if piece.positions == [[4,2], [4,3], [5,3], [4,4] ]: #T
            return ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd',
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd',
                       'ww', 'wwaa', 'wwdddd', 'wwa', 'wwddd', 'wwdd', 'wwd',
                       'www', 'wwwaa', 'wwwddd', 'wwwa', 'wwwdd', 'wwwd']
        elif piece.positions == [[4,2], [4,3], [4,4], [5,4] ]:#L
            return ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd', 
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd',
                       'ww', 'wwaa', 'wwdddd', 'wwa', 'wwddd', 'wwdd', 'wwd',
                       'www', 'wwwaa', 'wwwddd', 'wwwa', 'wwwdd', 'wwwd']
        elif piece.positions == [[3,3], [4,3], [3,4], [4,4] ]:#O
            return ['', 'aa', 'dd', 'a', 'd', 'ddd', 'dddd']
        elif piece.positions == [[4,2], [5,2], [4,3], [4,4] ]:#J
            return ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd', 
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd',
                       'wwaa', 'ww', 'wwdddd', 'wwa', 'wwddd', 'wwdd', 'wwd',
                       'www', 'wwwaa', 'wwwddd', 'wwwa', 'wwwdd', 'wwwd']
        elif piece.positions == [[4,2], [4,3], [5,3], [5,4] ]:#S
            return ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd',
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd']
        elif piece.positions == [[2,2], [3,2], [4,2], [5,2] ]:#I
            return ['', 'a', 'ddd', 'dd', 'd',
                       'w', 'waaa', 'wdddd', 'wddd', 'waa',  'wa', 'wdd', 'wd'] #tiramos acoes 'waaa', 'waa'
        else:#Z
            return ['', 'aa', 'dddd', 'a', 'ddd', 'dd', 'd',
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd']

    def get_piece_by_shape(self, piece_positions):
        if piece_positions == [[2, 1], [2, 2], [3, 2], [2, 3]]: #T
            return Piece([[4,2], [4,3], [5,3], [4,4] ])
        elif piece_positions == [[2, 1], [2, 2], [2, 3], [3, 3]]:#L
            return Piece([[4,2], [4,3], [4,4], [5,4] ])
        elif piece_positions == [[1, 2], [2, 2], [1, 3], [2, 3]]:#O
            return Piece([[3,3], [4,3], [3,4], [4,4] ])
        elif piece_positions == [[2, 1], [3, 1], [2, 2], [2, 3]]:#J
            return Piece([[4,2], [5,2], [4,3], [4,4] ])
        elif piece_positions == [[2, 1], [2, 2], [3, 2], [3, 3]]:#S
            return Piece([[4,2], [4,3], [5,3], [5,4] ])
        elif piece_positions == [[0, 1], [1, 1], [2, 1], [3, 1]]:#I
            return Piece([[2,2], [3,2], [4,2], [5,2] ])
        else:#Z
            return Piece([[4,2], [3,3], [4,3], [3,4] ])

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
        return (self.aggregate_height(state) * -0.510066) + (self.bumpiness(state) * -0.184483) + (self.holes(state)* -0.35663) + (self.completed_lines(state) * 0.555)
    
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        student = Student()
        next_pieces = []
        key = ''
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                ) 
                if len(key) == 0:
                    if next_pieces != state.get("next_pieces"):
                        next_pieces = state.get("next_pieces")
                        # receive game update, this must be called timely or your game will get out of sync with the server
                        # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                        #print("STATE ", state)
                        if state.get("piece") != None:
                            piece = Piece(state.get("piece"))
                            p = SearchProblem(student,piece)
                            #print("PECA NO STUDENT QUE ESTA A CAIR ", piece.plan )
                            key = p.search(state) + 's'
                            #print("Entrei pela 1 vez", key)
                            #print("KEYYYY   : ", key)
                            action = key[0]
                            #print("Vou enviar isto ", action)
                            key = key[1:]
                            await websocket.send(
                                json.dumps({"cmd": "key", "key": action})
                                
                            )  # send key command to server - you must implement this send in the AI agent
                else:
                    #print("Entrei ", key)
                    action = key[0]
                    #print("Vou enviar isto ", action)
                    key = key[1:]
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": action})
                        
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