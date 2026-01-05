from platform import node
from unicodedata import name
from lark import Lark, Transformer
import sys
import io
import contextlib

from matplotlib.pylab import pad

def run_compiled_code(python_code):
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(python_code, {})
    except Exception as e:
        return f"Runtime Error: {e}"
    return output_buffer.getvalue()




# =======================
# GRAMMAR
# =======================

grammar = r"""
start: stmt+

stmt: assign
    | print_stmt
    | while_stmt
    | for_stmt
    | func_def
    | break_stmt
    | continue_stmt
    | return_stmt

assign: NAME "itu" expr
print_stmt: "yap" expr

while_stmt: "kalo" expr ":" stmt+ "END"
for_stmt: "cmiiw" NAME "in" expr ":" stmt+ "END"

func_def: "imo" NAME "(" [params] ")" ":" stmt+ "END"

break_stmt: "burnout"
continue_stmt: "gas"
return_stmt: "stop" expr

params: NAME ("," NAME)*

?expr: expr "kurang" expr  -> lt
     | expr "lebih" expr   -> gt
     | expr "plus" term    -> add
     | expr "minus" term   -> sub
     | term

?term: term "kali" factor  -> mul
     | term "bagi" factor  -> div
     | factor

?factor: NUMBER
       | func_call
       | NAME
       | "(" expr ")"

func_call: NAME "(" [args] ")"
args: expr ("," expr)*


NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /\d+/

%import common.WS
%ignore WS

"""

# =======================
# AST NODES
# =======================

class Assign:
    def __init__(self, name, value): self.name, self.value = name, value

class Print:
    def __init__(self, expr): self.expr = expr

class While:
    def __init__(self, cond, body): self.cond, self.body = cond, body

class For:
    def __init__(self, var, limit, body):
        self.var, self.limit, self.body = var, limit, body

class FuncDef:
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body

class FuncCall:
    def __init__(self, name, args):
        self.name, self.args = name, args

class Break: pass
class Continue: pass

class Return:
    def __init__(self, value): self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class Var:
    def __init__(self, name): self.name = name

class Num:
    def __init__(self, value): self.value = value

# =======================
# AST BUILDER
# =======================

class ASTBuilder(Transformer):

    def start(self, args):
        return args

    def stmt(self, args):
        return args[0]

    def params(self, args):
        return args

    def assign(self, a):
        return Assign(a[0], a[1])

    def print_stmt(self, a):
        return Print(a[0])

    def while_stmt(self, a):
        return While(a[0], a[1:])
    def args(self, a):
        return a

    def for_stmt(self, a):
        return For(a[0], a[1], a[2:])

    def func_def(self, a):
        name = a[0]
        params = a[1] if isinstance(a[1], list) else []
        body = a[2:] if params else a[1:]
        return FuncDef(name, params, body)

    def func_call(self, a):
        name = a[0]
        args = a[1] if len(a) > 1 else []
        return FuncCall(name, args)

    def break_stmt(self, _): return Break()
    def continue_stmt(self, _): return Continue()
    def return_stmt(self, a): return Return(a[0])

    def add(self, a): return BinOp(a[0], "+", a[1])
    def sub(self, a): return BinOp(a[0], "-", a[1])
    def mul(self, a): return BinOp(a[0], "*", a[1])
    def div(self, a): return BinOp(a[0], "/", a[1])
    def lt(self, a): return BinOp(a[0], "<", a[1])
    def gt(self, a): return BinOp(a[0], ">", a[1])

    def NAME(self, n): return Var(str(n))
    def NUMBER(self, n): return Num(str(n))



# =======================
# CODE GENERATOR (PYTHON)
# =======================

class PythonCompiler:

    def emit(self, node, indent=0):
        pad = "    " * indent

        if isinstance(node, Assign):
            return f"{pad}{node.name.name} = {self.emit(node.value)}"

        if isinstance(node, For):
            code = f"{pad}for {node.var.name} in range({self.emit(node.limit)}):\n"
            for s in node.body:
                code += self.emit(s, indent + 1) + "\n"
            return code.rstrip()
        if isinstance(node, FuncCall):
            args = ", ".join(self.emit(a) for a in node.args)
            return f"{node.name.name}({args})"

        if isinstance(node, Print):
            return f"{pad}print({self.emit(node.expr)})"

        if isinstance(node, While):
            code = f"{pad}while {self.emit(node.cond)}:\n"
            for s in node.body:
                code += self.emit(s, indent + 1) + "\n"
            return code.rstrip()

        if isinstance(node, FuncDef):
            params = ", ".join(p.name for p in node.params)
            code = f"{pad}def {node.name.name}({params}):\n"
            for s in node.body:
                code += self.emit(s, indent + 1) + "\n"
            return code.rstrip()

        if isinstance(node, Break): return f"{pad}break"
        if isinstance(node, Continue): return f"{pad}continue"
        if isinstance(node, Return): return f"{pad}return {self.emit(node.value)}"

        if isinstance(node, BinOp):
            return f"{self.emit(node.left)} {node.op} {self.emit(node.right)}"

        if isinstance(node, Var): return node.name
        if isinstance(node, Num): return node.value

        raise Exception(f"Unknown node: {node}")

# =======================
# COMPILER DRIVER
# =======================

def compile_source(source_code):
    parser = Lark(grammar, parser="lalr")
    tree = parser.parse(source_code)
    ast = ASTBuilder().transform(tree)

    compiler = PythonCompiler()
    output = []

    for stmt in ast:
        output.append(compiler.emit(stmt))

    return "\n".join(output)

# =======================
# RUN
# =======================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python compiler.py <file.jaksel>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        source = f.read()

    python_code = compile_source(source)

    print("===== GENERATED CODE =====")
    print(python_code)
    print("==========================")

    with open("output.txt", "w") as f:
        f.write(python_code)

    print("Compilation finished → output.txt generated")
