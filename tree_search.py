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

        #verificar se nas bordas do view deixa uma coluna vazia para a peca I
        if self.piece.name == 'J' or self.piece.name == 'I' or self.piece.name == 'L': 
            high_column = [0,0,0,0,0,0,0,0]
            for x, y in stateGame["game"]:
                if 30 - y > high_column[x - 1]:
                    high_column[x - 1] = 30 - y

            firstColumn_heightRel = high_column[0] - high_column[1]
            lastColumn_heightRel = high_column[7] - high_column[6]

            if lastColumn_heightRel <=-4:
                if self.piece.name == 'L' and [[0, 1], [1, 1], [2, 1], [3, 1]] not in stateGame["next_pieces"]:
                    return 'wwdddds'
                elif self.piece.name == 'I':
                    return 'wdddds'
            elif firstColumn_heightRel <=-4:
                if self.piece.name == 'J'and [[0, 1], [1, 1], [2, 1], [3, 1]] not in stateGame["next_pieces"]:
                    return 'aaas'
                elif self.piece.name == 'I':
                    return 'waaas'

        #Determinar todas as possibilidades
        all_possibilities = []
        peçaOriginal = deepcopy(self.piece)
        for action in self.get_actions_by_shape(peçaOriginal):
            new_piece = self.domain.result(action, peçaOriginal)
            all_possibilities.append((new_piece, action ))
            peçaOriginal = deepcopy(self.piece)
        action = self.goal_test(all_possibilities, stateGame)
        return action 