import os
from tatsu.ast import AST
from pprint import pprint

# This works okay also
# def var(ast):
#     print("in var func", ast)
#     return 1

class var():
    def __init__(self, ast):
        self.ident = ast.ident
    def __repr__(self):
        return "<VAR " +  self.ident + ">"

def int_literal(literal):
    return int(literal)

def _default(*args):
    print("default" + str(args))
    return args[0]

#class number():
#    def __init__(self, ast):
#        return int(ast)

# def ev(ast, env):
    
    
    
