""" diffy.
    A simple symbolic differentiator in python.
    Bence Weisz 2024
"""

from enum import Enum
from typing import List

class DiffyNodeType(Enum):
    CONST = 0
    VAR = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    POW = 6
    LN = 7
    SIN = 8
    COS = 9
    TAN = 10
    E = 11
    PI = 12

class DiffyNode:
    type: DiffyNodeType
    args: List

    def __init__(self, type: DiffyNodeType, args: List) -> None:
        self.type = type
        self.args = args

    def __add__(self, other):
        return DiffyNode(DiffyNodeType.ADD, [self, other])
    
    def __sub__(self, other):
        return DiffyNode(DiffyNodeType.SUB, [self, other])
    
    def __mul__(self, other):
        return DiffyNode(DiffyNodeType.MUL, [self, other])
    
    def __truediv__(self, other):
        return DiffyNode(DiffyNodeType.DIV, [self, other])
    
    def __pow__(self, other):
        return DiffyNode(DiffyNodeType.POW, [self, other])
    
    def __repr__(self) -> str:
        if self.type == DiffyNodeType.CONST:
            return self.args[0]
        elif self.type == DiffyNodeType.VAR:
            return self.args[0]
        elif self.type == DiffyNodeType.ADD:
            return f"({self.args[0]} + {self.args[1]})"
        elif self.type == DiffyNodeType.SUB:
            return f"({self.args[0]} - {self.args[1]})"
        elif self.type == DiffyNodeType.MUL:
            return f"({self.args[0]} * {self.args[1]})"
        elif self.type == DiffyNodeType.DIV:
            return f"({self.args[0]} / {self.args[1]})"
        elif self.type == DiffyNodeType.POW:
            return f"({self.args[0]} ^ {self.args[1]})"
        elif self.type == DiffyNodeType.LN:
            return f"ln ({self.args[0]})"
        elif self.type == DiffyNodeType.SIN:
            return f"sin ({self.args[0]})"
        elif self.type == DiffyNodeType.COS:
            return f"cos ({self.args[0]})"
        elif self.type == DiffyNodeType.TAN:
            return f"tan ({self.args[0]})"
        elif self.type == DiffyNodeType.E:
            return "e"
        elif self.type == DiffyNodeType.PI:
            return "PI"
        
    def diffy(self):
        """ Derive the symbolic derivative of this DiffyNode. """
        if self.type == DiffyNodeType.CONST:
            return DiffyConst("0")
        elif self.type == DiffyNodeType.VAR:
            return DiffyConst("1")
        elif self.type == DiffyNodeType.ADD:
            return DiffyNode(DiffyNodeType.ADD, [self.args[0].diffy(), self.args[1].diffy()])
        elif self.type == DiffyNodeType.SUB:
            return DiffyNode(DiffyNodeType.SUB, [self.args[0].diffy(), self.args[1].diffy()])
        elif self.type == DiffyNodeType.MUL:
            return DiffyNode(
                DiffyNodeType.ADD,
                [
                    DiffyNode(DiffyNodeType.MUL, [self.args[0].diffy(), self.args[1]]),
                    DiffyNode(DiffyNodeType.MUL, [self.args[0], self.args[1].diffy()])
                ]
            )
        elif self.type == DiffyNodeType.DIV:
            return DiffyNode(
                DiffyNodeType.DIV,
                [
                    DiffyNode(
                        DiffyNodeType.SUB,
                        [
                            DiffyNode(DiffyNodeType.MUL, [self.args[0].diffy(), self.args[1]]),
                            DiffyNode(DiffyNodeType.MUL, [self.args[0], self.args[1].diffy()])
                        ]
                    ),
                    DiffyNode(
                        DiffyNodeType.POW,
                        [
                            self.args[1],
                            DiffyConst("2")
                        ]
                    )
                ]
            )
        elif self.type == DiffyNodeType.POW:
            if self.args[0].type == DiffyNodeType.CONST or self.args[0].type == DiffyNodeType.E or self.args[0].type == DiffyNodeType.PI:
                return DiffyNode(
                    DiffyNodeType.MUL,
                    [
                        DiffyNode(
                            DiffyNodeType.MUL,
                            [
                                DiffyNode(DiffyNodeType.LN, [self.args[0]]),
                                self
                            ]
                        ),
                        self.args[1].diffy()
                    ]
                )
            elif self.args[1].type == DiffyNodeType.CONST or self.args[1].type == DiffyNodeType.E or self.args[1].type == DiffyNodeType.PI:
                return DiffyNode(
                    DiffyNodeType.MUL,
                    [
                        DiffyNode(
                            DiffyNodeType.MUL,
                            [
                                self.args[1],
                                DiffyNode(
                                    DiffyNodeType.POW,
                                    [
                                        self.args[0],
                                        DiffyNode(DiffyNodeType.SUB, [self.args[1], DiffyConst("1")])
                                    ]
                                )
                            ]
                        ),
                        self.args[0].diffy()
                    ]
                )
            
    def simp(self):
        """ Simplify the DiffyNode. """
        if self.type == DiffyNodeType.ADD:
            if self.args[0].type == DiffyNodeType.CONST and self.args[0].args[0] == "0":
                return self.args[1]
            elif self.args[1].type == DiffyNodeType.CONST and self.args[1].args[0] == "0":
                return self.args[0]

class DiffyConst(DiffyNode):
    def __init__(self, const: str) -> None:
        super().__init__(DiffyNodeType.CONST, [const])

class DiffyVar(DiffyNode):
    def __init__(self, var: str) -> None:
        super().__init__(DiffyNodeType.VAR, [var])

class DiffyPI(DiffyNode):
    def __init__(self) -> None:
        super().__init__(DiffyNodeType.PI, [])

class DiffyE(DiffyNode):
    def __init__(self) -> None:
        super().__init__(DiffyNodeType.E, [])