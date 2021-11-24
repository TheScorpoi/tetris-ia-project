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
        #self.actions = ["left", "right", "down", "drop", "turn_right", "turn_left"]
        #self.actions = ['a', 'd', 'w', '', 's']
        self.actions = [ 'd', 'dw', 'dww', 'dwww', 'dd', 'ddw', 'ddww', 'ddwww', 'ddd', 'dddw', 'dddww', 'dddwww', 'dddd', 'ddddw', 'ddddww', 'ddddwww', 'dddd', 'ddddw', 'ddddww', 'ddddwww', 'ddddd', 'dddddw', 'dddddww', 'dddddwww', 'dddddd', 'ddddddw', 'ddddddww', 'ddddddwww',
            'a', 'aw', 'aww', 'awww', 'aa', 'aaw', 'aaww', 'aawww', 'aaa', 'aaaw', 'aaaww', 'aaawww', 'aaaa', 'aaaaw', 'aaaaww', 'aaaawww', 'aaaa', 'aaaaw', 'aaaaww', 'aaaawww', 'aaaaa', 'aaaaaw', 'aaaaaww', 'aaaaawww', 'aaaaaa', 'aaaaaaw', 'aaaaaaww', 'aaaaaawww', 'w', 'ww', 'www', '']

    def goal_test(self, all_possibilities, stateGame):
        return self.domain.satisfies(all_possibilities, stateGame)

     # procurar a solucao
    def search(self, stateGame,limit = math.inf):
        all_possibilities = []
        for action in self.actions:
            #print("Peca ", self.piece)
            new_piece = self.domain.result(action, deepcopy(self.piece))
            #print("Nova peca apos a acao ", action, " : ", new_piece)
            all_possibilities.append((deepcopy(new_piece), action))
        #print("ALL POSSIBILITIES (TEM QUE DAR cois dif)")
        #for c in all_possibilities:
            #print(f"{c[0]}")
        action = self.goal_test(all_possibilities, stateGame)
        return action 