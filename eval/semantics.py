
import os
from tatsu.ast import AST
from pprint import pprint

def s(x): str(x)

if int(os.environ.get('DEBUG', 0)):
  def debug(*strings):
    print("".join(map(str, strings)))
else:
  def debug(*strings):
    pass

class Percentage(float):
  pass

class Var():
  def __init__(self, name, env):
    self.name = name
    self.env = env

  def get(self):
    return self.env[self.name]

  def set(self, val):
    self.env[self.name] = val


class Semantics:
  def expression(self, ast):
    debug("** expression: ", ast)
    if isinstance(ast, AST):
      right = ast.right
      if isinstance(right, Percentage):
        right = ast.left * right / 100

      if ast.op == '+':
        return ast.left + right
      elif ast.op == '-':
        return ast.left - right
      else:
        raise Exception("WTF", ast.op)
    else:
      return ast

  def assignment(self, ast):
    ast.left.set(ast.right)
    return ast.right

  def term(self, ast):
    debug("** term: ", ast)
    if isinstance(ast, AST):
      right = ast.right
      if isinstance(right, Percentage):
        right = ast.right / 100
      if ast.op == '*' or ast.op == '×':
        return ast.left * right
      elif ast.op == '/' or ast.op == '÷':
        return ast.left / right
      else:
        raise Exception("WTF", ast.op)
    else:
      return ast

  def compound_expression(self, ast):
    return ast[1]

  def factor(self, ast):
    if isinstance(ast, AST):
      return ast.left ** ast.right
    else:
      return ast

  def number(self, ast):
    if "get" in ast.__dir__():
      return ast.get()
    else:
      return float(ast)

  def var(self, name):
    return Var(name, self.env)

  def pi(self, ast):
    return self.env["π"]

  def floatliteral(self, ast):
    f = float(ast.frac)
    if ast.intpart is not None:
      f += float(ast.intpart)
    return f

  def set_var(self, name, val):
    self.env[name] = val

  def percentage(self, ast):
    return Percentage(ast.val)
