#!/usr/bin/python3

import tatsu    # parser generator library
import pprint   # pretty-printer
import reprlib
from semantics import Semantics

class Grammar():

    def __init__(self, semantics=Semantics()):
        self.semantics = semantics
        self.vars = Grammar.init_namespace()
        self.semantics.vars = self.vars

    def set_var(self, name, val):
        self.vars[name] = val

    @classmethod
    def init_namespace(cls):
        import math
        return { "pi": math.atan2(0, -1),
                 "π": math.atan2(0, -1),
                 "it": None,
                 "e": math.exp(1),
                 }

    grammar = '''
@@grammar::EVAL

start = expression $ ;

expression = left:expression op:'+' right:term
           | left:expression op:'-' right:term
           | term
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

base = number | compound_expression;

compound_expression = '(' expression ')' ;

number = /\d+/ | pi | var;
pi = 'π' ;
var = ?'[a-zA-Z_]\w*';

'''

    parser = tatsu.compile(grammar, name="eval")

    def parse(self, expr):
        return self.parser.parse(expr, semantics=self.semantics)
