#!/usr/bin/python3

import tatsu    # parser generator library
import pprint   # pretty-printer
import reprlib
from semantics import Semantics
import math

class Grammar():

    def __init__(self, semantics=Semantics()):
        self.semantics = semantics
        self.semantics.env = Grammar.init_namespace()

    def set_var(self, name, val):
        self.semantics.set_var(name, val)

    @classmethod
    def init_namespace(cls):
        import math
        return { "pi": math.atan2(0, -1),
                 "π": math.atan2(0, -1),
                 "it": None,
                 "e": math.exp(1),

                 "sq": lambda x: x*x,
                 "sqrt": math.sqrt,
                 "sin": math.sin,
                 "cos": math.cos,
                 "tan": math.tan,
                 "exp": math.exp,
                 "log": math.log,

                 "int": int,
        }

    grammar = '''
@@grammar::EVAL

start = expression $ ;

expression = assignment
           | left:expression op:'+' right:term
           | left:expression op:'-' right:term
           | term
;

assignment = left:var '=' right:expression
;

term =   
         left:term op:'*' right:factor
       | left:term op:'×' right:factor
       | left:term op:'/' right:factor
       | left:term op:'÷' right:factor
       | factor
;

factor =
      left:base '**' right:factor 
    | left:base '^' right:factor
    | base; 

base = funcall | percentage | number | compound_expression;
compound_expression = '(' expression ')' ;

funcall = func:var '(' arg:expression ')';

percentage = val:(floatliteral | int) '%' ;

number = floatliteral | int | pi | var;
int = /\d+/;
floatliteral = [intpart:int] frac:decimal_frac;
decimal_frac = /\.\d+/;
pi = 'π' ;
var = ?'[a-zA-Z_]\w*';

'''

    parser = tatsu.compile(grammar, name="eval")

    def parse(self, expr):
        return self.parser.parse(expr, semantics=self.semantics)
