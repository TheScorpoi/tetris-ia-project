from copy import deepcopy
from shape import SHAPES, Shape

S = [
    [".....", ".....", "..11.", ".11..", "....."],
    [".....", "..1..", "..11.", "...1.", "....."],
]

Z = [
    [".....", ".....", ".11..", "..11.", "....."],
    [".....", "..1..", ".11..", ".1...", "....."],
]

I = [
    ["..1..", "..1..", "..1..", "..1..", "....."],
    [".....", "1111.", ".....", ".....", "....."],
]

O = [[".....", ".....", ".11..", ".11..", "....."]]


J = [
    [".....", ".1...", ".111.", ".....", "....."],
    [".....", "..11.", "..1..", "..1..", "....."],
    [".....", ".....", ".111.", "...1.", "....."],
    [".....", "..1..", "..1..", ".11..", "....."],
]

L = [
    [".....", "...1.", ".111.", ".....", "....."],
    [".....", "..1..", "..1..", "..11.", "....."],
    [".....", ".....", ".111.", ".1...", "....."],
    [".....", ".11..", "..1..", "..1..", "....."],
]

T = [
    [".....", "..1..", ".111.", ".....", "....."],
    [".....", "..1..", "..11.", "..1..", "....."],
    [".....", ".....", ".111.", "..1..", "....."],
    [".....", "..1..", ".11..", "..1..", "....."],
]

class Piece:

    def __init__(self, positions):
        self.positions = positions
        self.plan = None
        self.index_plan = 1
        if [[4,2], [4,3], [5,3], [4,4] ]  == positions:
            self.plan = T
            self.name = 'T'
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif [[4,2], [4,3], [4,4], [5,4] ]  == positions:
            self.plan = L
            self.name = 'L'
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif [[3,3], [4,3], [3,4], [4,4] ]  == positions:
            self.plan = O
            self.name = 'O'
            self._pos = [[0,0], [0, 0], [0, 0], [0, 0]]
        elif [[4,2], [5,2], [4,3], [4,4] ]  == positions:
            self.plan = J
            self.name = 'J'
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif [[4,2], [4,3], [5,3], [5,4] ]  == positions:
            self.plan = S
            self.name = 'S'
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif [[2,2], [3,2], [4,2], [5,2] ]  == positions:
            self.plan = I
            self.name = 'I'
            self._pos = [[2,5], [2, 1], [2, 1], [2, 1]]
        elif [[4,2], [3,3], [4,3], [3,4] ]  == positions:
            self.plan = Z
            self.name = 'Z'
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
            
        
    def verify(self, piece1, piece2):
        if piece1.sort() == piece2.sort():
            return True
        piece1_aux = deepcopy(piece1) 
        for incr in range(1, 28):
            piece1_aux = [(cx , cy + 1) for cx, cy in piece1_aux]
            if piece1_aux.sort() == piece2.sort():
                return True
        return False


    def set_pos(self, x, y):
        x = int(x)
        y = int(y)
        self.positions = [
            [cx + x , cy + y ] for cx, cy in self.positions
        ]

        for index in range(len(self._pos)):
            self._pos[index][0] = self._pos[index][0] + x 
            self._pos[index][1] = self._pos[index][1] + y 
    def rotate(self):
        self.update_plan()
        self.positions = [
            [x, y]
            for y, line in enumerate(self.plan[self.index_plan])
            for x, pos in enumerate(line)
            if pos == "1"
        ]

        for index in range(len(self._pos)):
            self.positions[index][0] = self.positions[index][0] + self._pos[index][0] 
            self.positions[index][1] = self.positions[index][1] + self._pos[index][1] 

    def update_plan(self):
        self.index_plan += 1
        if self.index_plan >= len(self.plan):
            self.index_plan = 0

    def chek_update(self, positions_temp):
        flag = True 
        for coord in positions_temp:
            if coord[0] < 1 or coord[0] > 8:
                flag = False
            elif coord[1] < 0 or coord[1] > 29:
                flag = False
        return flag

    def translate(self, x, y):
        self.set_pos(x, y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self.set_pos(x, self._y)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self.set_pos(self._x, y)

    def __str__(self) -> str:
        return f"Shape() -> {self.positions} -> {self.plan}"