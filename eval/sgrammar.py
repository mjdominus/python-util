#!/usr/bin/python3


grammar = '''
@@grammar::EVAL

start = expression $ ;

expression::Expr = left:expression op:'+' right:term
           | left:expression op:'-' right:term
           | @:term
;

term::Term =   
         left:term op:'*' right:factor
       | left:term op:'×' right:factor
       | left:term op:'/' right:factor
       | left:term op:'÷' right:factor
       | @:factor
;

factor::Factor =
      left:base '**' right:factor 
    | left:base '^' right:factor
    | @:base; 

base::BASE = var | number | compound_expression;
compound_expression = '(' @:expression ')' ;

number::Number = int_literal;
int_literal::IntLit = /\d+/;
var::VAR = ident:?'[a-zA-Z_]\w*';

'''

