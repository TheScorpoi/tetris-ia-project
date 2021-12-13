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
        self.dic = {}
        self.next_actions = []  #proximas acoes, calculadas atraves do lookhead

    def empty_dic(self):
        self.dic = {}

    def empty_next_actions(self):
        self.next_actions = []

    def is_empty_next_actions(self):
        return self.next_actions == []
    
    def result(self, actions, piece): #Resultado da peca depois das acaos actions
        for action in actions:
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
        
    def satisfies(self, all_possibilities, stateGame, isWith_nextPieces): # Resultado da melhor acao com base no estado do jogo 
        action_heuristic = {}
        for piece_action in all_possibilities:
            piece = piece_action[0]
            positions_piece = piece.positions #posicoes da peca sem a acao 's'

            #Simular a peca lá em baixo:
            miny_instateGame = [30, 30, 30, 30, 30, 30, 30, 30]          
            if stateGame["game"] != []:
                for c in stateGame["game"]:
                    if miny_instateGame[c[0] - 1] > c[1]:
                        miny_instateGame[c[0] - 1] = c[1]
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
            if len(proximas_pecas) == 3 and isWith_nextPieces: # Calcular as acoes das duas proximas pecas juntas
                new_game = {}
                new_game['game'] = future_stateGame
                new_game['next_pieces'] = stateGame['next_pieces'][1:]    

                #Calcular a melhor acao da segunda peca
                all_pos = []    
                peçaOriginal = deepcopy(self.get_piece_by_shape(proximas_pecas[0]))
                new_game['piece'] = peçaOriginal.positions
                for action in self.get_actions_by_shape(peçaOriginal):
                    new_piece = self.result(action, peçaOriginal)
                    all_pos.append((new_piece, action))
                    peçaOriginal = deepcopy(self.get_piece_by_shape(proximas_pecas[0]))
                action = self.satisfies(all_pos, new_game, True)

                positions_result = self.result(action,peçaOriginal).positions
                
                #Simular a segunda peca lá em baixo:
                miny_instateGame2 = [30, 30, 30, 30, 30, 30, 30, 30]          
                if new_game['game'] != []:
                    for c in new_game['game']:
                        if miny_instateGame2[c[0] - 1] > c[1]:
                            miny_instateGame2[c[0] - 1] = c[1]
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
                #Calcular a heuristica das acoes da primeira peca e segunda, guardar num dicionario com chave a acao da primeira peca
                action_heuristic[piece_action[1]] = self.heuristic(new_game['game'] + positions_result_bottom)
                #Guardar a acao da segunda peca num dicionario com chave a primeira peca
                self.dic[piece_action[1]] = action
            else:
                #Calcular a heuristica 
                action_heuristic[piece_action[1]] = self.heuristic(future_stateGame)
        
        #Calcular a melhor heuristica e guardar a acao respetiva
        min_heuristic = -10000
        action_to_do = 's'
        for key in action_heuristic:
            if action_heuristic[key] > min_heuristic:
                min_heuristic = action_heuristic[key]
                action_to_do = key 
        
        if len(stateGame['next_pieces']) == 3 and isWith_nextPieces:
            #Caso seja analisado o lookhead, guardar a acao da segunda peca na lista das proximas acoes
            self.next_actions.append(self.dic[action_to_do])
        
        return action_to_do # returnar a melhor acao

    def get_actions_by_shape(self, piece):
        if piece.positions == [[4,2], [4,3], [5,3], [4,4] ]: #T
            return ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds',
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds',
                       'wws', 'wwaas', 'wwdddds', 'wwas', 'wwddds', 'wwdds', 'wwds',
                       'wwws', 'wwwaas', 'wwwddds', 'wwwas', 'wwwdds', 'wwwds']
        elif piece.positions == [[4,2], [4,3], [4,4], [5,4] ]:#L
            return ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds', 
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds',
                       'wws', 'wwaas', 'wwdddds', 'wwas', 'wwddds', 'wwdds', 'wwds',
                       'wwws', 'wwwaas', 'wwwddds', 'wwwas', 'wwwdds', 'wwwds']
        elif piece.positions == [[3,3], [4,3], [3,4], [4,4] ]:#O
            return ['s', 'aas', 'dds', 'as', 'ds', 'ddds', 'dddds']
        elif piece.positions == [[4,2], [5,2], [4,3], [4,4] ]:#J
            return ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds', 
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds',
                       'wwaas', 'wws', 'wwdddds', 'wwas', 'wwddds', 'wwdds', 'wwds',
                       'wwws', 'wwwaas', 'wwwddds', 'wwwas', 'wwwdds', 'wwwds']
        elif piece.positions == [[4,2], [4,3], [5,3], [5,4] ]:#S
            return ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds',
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds']
        elif piece.positions == [[2,2], [3,2], [4,2], [5,2] ]:#I
            return ['s', 'as', 'ddds', 'dds', 'ds',
                       'ws', 'waaas', 'wdddds', 'wddds', 'waas',  'was', 'wdds', 'wds'] #tiramos acoes 'waaa', 'waa'
        else:#Z
            return ['s', 'aas', 'dddds', 'as', 'ddds', 'dds', 'ds',
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds']

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
        return (self.aggregate_height(state) * -0.510066) + (self.bumpiness(state) * -0.184483) + (self.holes(state)* -0.35663) + (self.completed_lines(state) * 0.760666)
    
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        student = Student()
        jogo = [] #ultimo state.get("game") analisado
        next_pieces = [] #ultimo next_pieces analisado
        key = ''    #acoes que a search retorna 
        flag_firstTime = True 
        duration = 0    #maxima duracao da search com lookhead implementada
        flag = True
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                ) 

                if len(key) == 0: # Chmar a search quando n tivermos mais acoes para enviar
                    if (jogo != state.get("game") and next_pieces != state.get("next_pieces") ) or flag_firstTime: #verifcar se a ultima peca analisada já realizou as acoes
                        if state.get("piece") != None:  
                            jogo = state.get("game")
                            next_pieces = state.get("next_pieces")
                            if student.is_empty_next_actions(): #verificar se ja determinamos as proximas acoes
                                piece = Piece(state.get("piece"))
                                if piece.plan != None:  #verificar se identificamos bem a peca
                                    student.empty_dic() #limpar variaveis do student para a nova pesquisa
                                    p = SearchProblem(student,piece, duration)
                                    inicio = time.time()
                                    key = p.search(state)
                                    if time.time() - inicio > duration: #atualiazar a maxima duracao da implementacao do lookhead
                                        duration = time.time() - inicio
                            else:
                                key = student.next_actions[0]  #obter a proxima acao, determinada pelo lookhead
                                student.empty_next_actions()   #limpar as proximas acoes
                            flag_firstTime = False
                else:
                    action = key[0] #obter a proxima acao
                    key = key[1:]   

                    if duration > 0.2 and not flag: #Enviar para o server sem a implementacao do lookhead
                        await websocket.send(
                            json.dumps({"cmd": "key", "key": action})
                        )  # send key command to server - you must implement this send in the AI agent
                    else: #Enviar para o server com a implementacao do lookhead
                        state = json.loads(
                            await websocket.recv()
                        ) 
                        if jogo == state.get("game") and next_pieces == state.get("next_pieces"): #verificar se a peca ainda n caiu 
                            await websocket.send(
                                json.dumps({"cmd": "key", "key": action})
                            )  # send key command to server - you must implement this send in the AI agent
                        else:   #se a peca ja caiu descartar as acoes guardadas
                            key = ''
                            student.empty_next_actions()
                        if duration > 0.2:
                            flag = False
                            
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