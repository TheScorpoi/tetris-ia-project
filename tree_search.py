from abc import ABC, abstractmethod
import math

class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, action, positions):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass
    
    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, positions):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, positions_initial):
        self.domain = domain
        self.positions_initial = positions_initial
        #self.actions = ["left", "right", "down", "drop", "turn_right", "turn_left"]
        self.actions = ['a']

    def goal_test(self, positions):
        return self.domain.satisfies(positions)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, parent, positions): 
        self.parent = parent
        self.positions = positions 
        self.final = False
        self.cost = 0 
        self.heuristic = 0
        if parent == None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def __str__(self):
        return "no(" + "," + str(self.parent) + ")"
    
    def __repr__(self):
        return str(self)
    
# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(None, problem.positions_initial)
        #root.heuristic = self.problem.domain.heuristic(root.state, self.problem.goal)
        self.open_nodes = [('', root)]
        self.strategy = strategy
        self.solution = None
        self.length = 0
        self.non_terminals = 0
        self.cost = 0
        

    # obter o caminho da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node]
        path = self.get_path(node.parent)
        path += [node]
        return(path)

    # procurar a solucao
    def search(self, limit = math.inf):
        while self.open_nodes != []:
            node = self.open_nodes[0][1]
            action = self.open_nodes.pop(0)[0]
            if self.problem.goal_test(node.positions):
                self.solution = node
                self.length = len(self.get_path(node)) - 1
                self.terminals = len(self.open_nodes) + 1
                #self.avg_branching = round((self.terminals+self.non_terminals-1)/self.non_terminals, 2)
                self.cost = node.cost
                return action
            lnewnodes = []
            self.non_terminals+=1
            for action in self.problem.actions:
                new_positions = self.problem.domain.result(node.state, action, node.positions)
                if new_positions != []:
                    newnode = SearchNode(node, new_positions)
                    if (not self.inParent(newnode)) and node.depth < limit:
                        #newnode.cost = node.cost + self.problem.domain.cost(node.state, (node.state, newstate))
                        #newnode.heuristic = self.problem.domain.heuristic(newnode.state, self.problem.goal)
                        lnewnodes.append((action,newnode))
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.heuristic + node.cost)

    #verificar se node já foi pai no caminho que estamos a verificar
    def inParent(self,node):
        nos = self.get_path(node)
        lastNo = nos.pop(-1)
        if lastNo in nos:
            return True
        return False