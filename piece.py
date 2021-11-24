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

    def __init__(self, positions):
        self.positions = positions
        self.plan = None
        #print("positions rere", positions)
        if positions == [[4,2], [4,3], [5,3], [4,4] ]:
            self.plan = T
        elif positions == [[4,2], [4,3], [4,4], [5,4] ]:
            self.plan = L
        elif positions == [[3,3], [4,3], [3,4], [4,4] ]:
            self.plan = O
        elif positions == [[4,2], [5,2], [4,3], [4,4] ]:
            self.plan = J
        elif positions == [[4,2], [4,3], [5,3], [5,4] ]:
            self.plan = S
        elif positions == [[2,2], [3,2], [4,2], [5,2] ]:
            self.plan = I
        elif positions == [[4,2], [3,3], [4,3], [3,4] ]:
            self.plan = Z
        else:
            self.plan = Piece.lastPlan
        
        Piece.lastPlan = self.plan
        self.rotation = 0
        self._x = 0
        self._y = 0

    def set_pos(self, x, y):
        x = int(x)
        y = int(y)
        positions_temp = [
            (cx + x - self._x, cy + y - self._y) for cx, cy in self.positions
        ]

        if self.chek_update(positions_temp):
            self.positions = positions_temp
            self._x = x
            self._y = y


    def rotate(self, step=1):
        self.rotation = (self.rotation + step) % len(self.plan)
        positions_temp = [
            (self._x + x, self._y + y)
            for y, line in enumerate(self.plan[self.rotation])
            for x, pos in enumerate(line)
            if pos == "1"
        ]

        if self.chek_update(positions_temp):
            self.positions = positions_temp

    def chek_update(self, positions_temp):
        flag = True 
        for coord in positions_temp:
            if coord[0] < 1 or coord[0] > 8:
                flag = False
            elif coord[1] < 0 or coord[1] > 29:
                flag = False
        return flag

    def translate(self, x, y):
        self.set_pos(self._x + x, self._y + y)

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
        return f"Shape({self._x},{self._y}) -> {self.positions} -> {self.plan}"