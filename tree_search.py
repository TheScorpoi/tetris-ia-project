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
    def __init__(self, domain, piece):
        self.domain = domain
        self.piece = piece
        #self.actions = ['w', 'ww', 'www', 'wwwa', 'wwwaw', 'wwwaww', 'wwwawww', 'wwwawwwa', 'wwwawwww', 'wwwawwwwa', 'wwwawwwwaw', 'wwwawwwwaww', 'wwwawwwwawww','d', 'dw', 'dww', 'dwww', 'dwwwd', 'dwwwdw', 'dwwwdww', 'dwwwdwww', 'dwwwdwww', 'dwwwdwwwd']                    
        #self.actions = [[''],['a'], ['a','a'],['a','a','a'],['d'], ['d','d'],['d','d','d']]
        self.actions = ['a', 'aa', 'aaa', 'd', 'dd' 'ddd', 'dddd', '',
                        'aw', 'aaw', 'aaaw', 'dw', 'ddw' 'dddw', 'ddddw' ]
        
    def goal_test(self, all_possibilities, stateGame):
        return self.domain.satisfies(all_possibilities, stateGame)

     # procurar a solucao
    def search(self, stateGame,limit = math.inf):
        all_possibilities = []
        peçaOriginal = deepcopy(self.piece)
        for action in self.actions:
            #print("Peca ", self.piece)
            new_piece = self.domain.result(action, peçaOriginal)
            #print("Nova peca apos a acao ", action, " : ", new_piece)
            all_possibilities.append((deepcopy(new_piece), action))
            peçaOriginal = deepcopy(self.piece)
        #print("ALL POSSIBILITIES (TEM QUE DAR cois dif)")
        #for c in all_possibilities:
            #print(f"{c[0]}")
        action = self.goal_test(all_possibilities, stateGame)
        return action 