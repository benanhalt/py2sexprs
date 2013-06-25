import sys
import _ast
from ast import parse

from generics import generic, method, call_next_method

class KeyWord(str):
    def pprint(self, indent=0):
        return ':%s' % self

class String(str):
    def pprint(self, indent=0):
        return '"%s"' % self.replace('\\', '\\\\').replace('"', '\\"')

class Int(int):
    def pprint(self, indent=0):
        return str(self)

class List(list):
    def pprint(self, indent=0):
        indent += 1
        if len(self) < 2:
            return '(%s)' % ' '.join(i.pprint(indent) for i in self)

        return '(%s)' % ('\n' + ' '*indent).join(i.pprint(indent) for i in self)

@generic
def to_list(ast_node):
    pass

@method(to_list)
def object_to_list(obj: object):
    return obj.__class__

@method(to_list)
def ast_to_list(node: _ast.AST):
    l = List([KeyWord(node.__class__.__name__)])
    l.extend(to_list(getattr(node, field)) for field in node._fields)
    return l

@method(to_list)
def list_to_list(l: list):
    return List(to_list(i) for i in l)

@method(to_list)
def none_to_list(n: None.__class__):
    return KeyWord('None')

@method(to_list)
def str_to_list(s: str):
    return String(s)

@method(to_list)
def int_to_list(n: int):
    return Int(n)

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        ast = parse(f.read())
    print(to_list(ast).pprint())
