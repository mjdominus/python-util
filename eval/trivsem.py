
import tatsu

class trivsem():
    def _default(self, ast, *rest, **kw):
        print("sem func (", ast, ") ", rest, kw)
        return MyAST(ast)

class MyAST(tatsu.ast.AST):
    pass
