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
        self.actions = []
        
    def goal_test(self, all_possibilities, stateGame):
        return self.domain.satisfies(all_possibilities, stateGame)
    
    def get_actions_by_shape(self, piece):
        if piece.positions == [[4,2], [4,3], [5,3], [4,4] ]: #T
            self.actions = ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd',
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd',
                       'ww', 'wwaa', 'wwdddd', 'wwa', 'wwddd', 'wwdd', 'wwd',
                       'www', 'wwwaa', 'wwwddd', 'wwwa', 'wwwdd', 'wwwd']
        elif piece.positions == [[4,2], [4,3], [4,4], [5,4] ]:#L
            self.actions = ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd', 
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd',
                       'ww', 'wwaa', 'wwdddd', 'wwa', 'wwddd', 'wwdd', 'wwd',
                       'www', 'wwwaa', 'wwwddd', 'wwwa', 'wwwdd', 'wwwd']
        elif piece.positions == [[3,3], [4,3], [3,4], [4,4] ]:#O
            self.actions = ['', 'aa', 'dd', 'a', 'd', 'ddd, dddd']
        elif piece.positions == [[4,2], [5,2], [4,3], [4,4] ]:#J
            self.actions = ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd', 
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd',
                       'wwaa', 'ww', 'wwdddd', 'wwa', 'wwddd', 'wwdd', 'wwd',
                       'www', 'wwwaa', 'wwwddd', 'wwwa', 'wwwdd', 'wwwd']
        elif piece.positions == [[4,2], [4,3], [5,3], [5,4] ]:#S
            self.actions = ['', 'aaa', 'ddd', 'aa', 'dd', 'a', 'd',
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd']
        elif piece.positions == [[2,2], [3,2], [4,2], [5,2] ]:#I
            self.actions = ['', 'a', 'ddd', 'dd', 'd',
                       'w', 'waaa', 'wdddd', 'waa', 'wddd', 'wa', 'wdd', 'wd']
        elif piece.positions == [[4,2], [3,3], [4,3], [3,4] ]:#Z
            self.actions = ['', 'aa', 'dddd', 'a', 'ddd', 'dd', 'd',
                       'w', 'waa', 'wddd', 'wa', 'wdd', 'wd']
        return self.actions        
        

     # procurar a solucao
    def search(self, stateGame,limit = math.inf):
        all_possibilities = []
        peçaOriginal = deepcopy(self.piece)
        for action in self.get_actions_by_shape(peçaOriginal):
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