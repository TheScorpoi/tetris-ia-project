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
    lastPlan = None
    lastPos = None

    def __init__(self, positions):
        self.positions = positions
        self.plan = None
        self.index_plan = 1
        #print("positions rere", positions)
        if positions == [[4,2], [4,3], [5,3], [4,4] ]:
            self.plan = T
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif positions == [[4,2], [4,3], [4,4], [5,4] ]:
            self.plan = L
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif positions == [[3,3], [4,3], [3,4], [4,4] ]:
            self.plan = O
            self._pos = [[0,0], [0, 0], [0, 0], [0, 0]]
        elif positions == [[4,2], [5,2], [4,3], [4,4] ]:
            self.plan = J
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif positions == [[4,2], [4,3], [5,3], [5,4] ]:
            self.plan = S
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        elif positions == [[2,2], [3,2], [4,2], [5,2] ]:
            self.plan = I
            self._pos = [[2,5], [2, 1], [2, 1], [2, 1]]
        elif positions == [[4,2], [3,3], [4,3], [3,4] ]:
            self.plan = Z
            self._pos = [[2,1], [2, 1], [2, 1], [2, 1]]
        else:
            self.plan = Piece.lastPlan
            self._pos = [[2,5], [2, 1], [2, 1], [2, 1]]
        
        Piece.lastPlan = self.plan
        Piece.lastPos = self._pos

    def set_pos(self, x, y):
        x = int(x)
        y = int(y)
        self.positions = [
            [cx + x , cy + y ] for cx, cy in self.positions
        ]

        for index in range(len(self._pos)):
            self._pos[index][0] = self._pos[index][0] + x 
            self._pos[index][1] = self._pos[index][1] + y 

        '''
        if not self.chek_update(self.positions):
            print("--------------ENTREI NO CHECK UPDATE COM TRANSLATE----------------------")
        '''
        
    def rotate(self):
        #self.rotation = (self.rotation + step) % len(self.plan)
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



        '''
        if not self.chek_update(self.positions):
            self.rotation = (self.rotation - 1) % len(self.plan)
            self.positions = [
                [self._x + x, self._y + y]
                for y, line in enumerate(self.plan[self.rotation])
                for x, pos in enumerate(line)
                if pos == "1"
            ]
        '''

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