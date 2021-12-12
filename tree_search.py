from abc import ABC, abstractmethod
from copy import deepcopy
import math
import time

class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, action, piece):
        pass
    
    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, piece):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, piece, duration):
        self.domain = domain
        self.piece = piece
        #self.actions = ['w', 'ww', 'www', 'wwwa', 'wwwaw', 'wwwaww', 'wwwawww', 'wwwawwwa', 'wwwawwww', 'wwwawwwwa', 'wwwawwwwaw', 'wwwawwwwaww', 'wwwawwwwawww','d', 'dw', 'dww', 'dwww', 'dwwwd', 'dwwwdw', 'dwwwdww', 'dwwwdwww', 'dwwwdwww', 'dwwwdwwwd']                    
        #self.actions = [[''],['a'], ['a','a'],['a','a','a'],['d'], ['d','d'],['d','d','d']]
        self.actions = []
        self.duration = duration
        
    def goal_test(self, all_possibilities, stateGame):
        if self.duration > 0.2:
            return self.domain.satisfies(all_possibilities, stateGame, False)
        return self.domain.satisfies(all_possibilities, stateGame, True)

    def get_actions_by_shape(self, piece):
        if piece.name == 'T':
            self.actions = ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds',
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds',
                       'wws', 'wwaas', 'wwdddds', 'wwas', 'wwddds', 'wwdds', 'wwds',
                       'wwws', 'wwwaas', 'wwwddds', 'wwwas', 'wwwdds', 'wwwds']
        elif piece.name == 'L':
            self.actions = ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds', 
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds',
                       'wws', 'wwaas', 'wwdddds', 'wwas', 'wwddds', 'wwdds', 'wwds',
                       'wwws', 'wwwaas', 'wwwddds', 'wwwas', 'wwwdds', 'wwwds']
        elif piece.name == 'O':
            self.actions = ['s', 'aas', 'dds', 'as', 'ds', 'ddds', 'dddds']
        elif piece.name == 'J':
            self.actions = ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds', 
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds',
                       'wwaas', 'wws', 'wwdddds', 'wwas', 'wwddds', 'wwdds', 'wwds',
                       'wwws', 'wwwaas', 'wwwddds', 'wwwas', 'wwwdds', 'wwwds']
        elif piece.name == 'S':
            self.actions = ['s', 'aaas', 'ddds', 'aas', 'dds', 'as', 'ds',
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds']
        elif piece.name == 'I':
            self.actions = ['s', 'as', 'ddds', 'dds', 'ds',
                       'ws', 'waaas', 'wdddds', 'wddds', 'waas',  'was', 'wdds', 'wds'] #tiramos acoes 'waaa', 'waa'
        elif piece.name == 'Z':
            self.actions = ['s', 'aas', 'dddds', 'as', 'ddds', 'dds', 'ds',
                       'ws', 'waas', 'wddds', 'was', 'wdds', 'wds']
        return self.actions        
        

     # procurar a solucao
    def search(self, stateGame,limit = math.inf):
        all_possibilities = []
        peçaOriginal = deepcopy(self.piece)
        print("Peca ", peçaOriginal)
        #print("--------------------INICIO----------------------------")
        for action in self.get_actions_by_shape(peçaOriginal):
            #print("Peca ", peçaOriginal)
            new_piece = self.domain.result(action, peçaOriginal)
            #print("Nova peca apos a acao ", action, " : ", new_piece)
            all_possibilities.append((new_piece, action ))
            peçaOriginal = deepcopy(self.piece)
        #print("--------------------FIM----------------------------")
        print("ALL POSSIBILITIES antes do goal_test")
        for c in all_possibilities:
            print(f"{c[0]}")
        action = self.goal_test(all_possibilities, stateGame)
        #print("Retornei esta acao ", action)
        return action 