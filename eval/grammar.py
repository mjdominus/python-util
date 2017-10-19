#!/usr/bin/python3

import tatsu    # parser generator library
import pprint   # pretty-printer
import reprlib
from semantics import Semantics

class Grammar():

    def __init__(self, semantics=Semantics()):
        self.semantics = semantics
    
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

factor = number | compound_expression;

compound_expression = '(' expression ')' ;

number = /\d+/;

'''

    parser = tatsu.compile(grammar, name="eval")

    def parse(self, expr):
        return self.parser.parse(expr, semantics=self.semantics)
