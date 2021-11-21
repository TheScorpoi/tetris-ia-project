from shape import SHAPES, Shape


class Piece:
    
    def __init__(self, positions):
        self.positions = positions
        shape = None
        if self.positions == [[4,2], [4,3], [5,3], [4,4] ]:
            shape = Shape(SHAPES.T)
        elif self.positions == [[4,2], [4,3], [4,4], [5,4] ]:
            shape = Shape(SHAPES.L)
        elif self.positions == [[3,3], [4,3], [3,4], [4,4] ]:
            shape = Shape(SHAPES.O)
        elif self.positions == [[4,2], [5,2], [4,3], [4,4] ]:
            shape = Shape(SHAPES.J)
        elif self.positions == [[4,2], [4,3], [5,3], [5,4] ]:
            shape = Shape(SHAPES.S)
        elif self.positions == [[2,2], [3,2], [4,2], [5,2] ]:
            shape = Shape(SHAPES.I)
        elif self.positions == [[4,2], [3,3], [4,3], [3,4] ]:
            shape = Shape(SHAPES.Z)
        print(shape)

    