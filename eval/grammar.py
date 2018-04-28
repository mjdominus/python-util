#!/usr/bin/python3

import tatsu    # parser generator library
import pprint   # pretty-printer
import reprlib
from semexp import semexp
import math

class Grammar():

    def __init__(self):
        pass

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
var = ident:?'[a-zA-Z_]\w*';

'''

    parser = tatsu.compile(grammar, name="eval")

    def parse(self, expr):
        return self.parser.parse(expr, semantics=semexp())
    
