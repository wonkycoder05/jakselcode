from lark import Lark, Transformer


#   GRAMMAR — INDONESIAN SLANG PYTHON

grammar = r"""
start: statement+

?statement: set_stmt
          | print_stmt
          | if_stmt
          | while_stmt
          | for_stmt
          | func_def
          | func_call
          | break_stmt

set_stmt: "SET" NAME expr
print_stmt: "yap" expr

if_stmt: "IF" expr ":" statement+ "END"

while_stmt: "kalo" expr ":" statement+ "END"

for_stmt: "cmiiw" NAME "in" expr ":" statement+ "END"

func_def: "imo" NAME "(" [param_list] ")" ":" statement+ "END"
func_call: "call" NAME "(" [arg_list] ")"

param_list: NAME ("," NAME)*
arg_list: expr ("," expr)*

break_stmt: "burnout"

?expr: comparison

?comparison: arith_expr (COMP_OP arith_expr)?
COMP_OP: ">" | "<" | ">=" | "<=" | "==" | "!="

?arith_expr: arith_expr "+" term   -> add
            | arith_expr "-" term  -> sub
            | term

?term: term "*" factor -> mul
     | term "/" factor -> div
     | factor

?factor: NUMBER        -> number
       | STRING        -> string
       | NAME          -> var
       | "(" expr ")"

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: ESCAPED_STRING
NUMBER: /-?\d+(\.\d+)?/

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
%ignore /#.*/ 
"""


#   RUNTIME

GLOBAL = {}
FUNCTIONS = {}
BREAK_FLAG = False



#   INTERPRETER

class Interpreter(Transformer):

    # ===== VALUES =====
    def number(self, n):
        return float(n[0]) if "." in n[0] else int(n[0])

    def string(self, s):
        return s[0][1:-1]

    def var(self, n):
        return GLOBAL.get(n[0], 0)

    # ===== MATH =====
    def add(self, a): return a[0] + a[1]
    def sub(self, a): return a[0] - a[1]
    def mul(self, a): return a[0] * a[1]
    def div(self, a): return a[0] / a[1]

    # ===== COMPARISON =====
    def comparison(self, args):
        if len(args) == 1:
            return args[0]
        left, op, right = args
        # Normalize op: it can be a Token, a Tree, or a plain string
        from lark.tree import Tree

        if isinstance(op, Tree):
            op = op.children[0] if op.children else ""

        op = str(op)

        return {
            ">": left > right,
            "<": left < right,
            ">=": left >= right,
            "<=": left <= right,
            "==": left == right,
            "!=": left != right
        }[op]

    # ===== SET =====
    def set_stmt(self, args):
        name, val = args
        GLOBAL[name] = val

    # ===== PRINT =====
    def print_stmt(self, args):
        print(args[0])

    # ===== IF =====
    def if_stmt(self, args):
        cond = args[0]
        body = args[1:]
        if cond:
            for stmt in body:
                pass

    # ===== WHILE (kalo) =====
    def while_stmt(self, args):
        global BREAK_FLAG
        cond = args[0]
        body = args[1:]

        while cond:
            for stmt in body:
                if BREAK_FLAG:
                    BREAK_FLAG = False
                    return
            cond = args[0]

    # ===== FOR (cmiiw) =====
    def for_stmt(self, args):
        varname, iterable, *body = args
        try:
            loop_items = iterable
        except:
            return

        for item in loop_items:
            GLOBAL[varname] = item
            for stmt in body:
                pass

    # ===== BREAK =====
    def break_stmt(self, _):
        global BREAK_FLAG
        BREAK_FLAG = True

    # ===== FUNCTION DEF =====
    def func_def(self, args):
        name = args[0]
        params = args[1] if isinstance(args[1], list) else []
        body = args[2:]
        FUNCTIONS[name] = (params, body)

    # ===== FUNCTION CALL =====
    def func_call(self, args):
        name = args[0]
        values = args[1] if isinstance(args[1], list) else []

        params, body = FUNCTIONS[name]

        backup = GLOBAL.copy()

        for p, v in zip(params, values):
            GLOBAL[p] = v

        for stmt in body:
            pass

        GLOBAL.update(backup)



#   RUNNER

def run(code):
    parser = Lark(grammar, start="start", parser="lalr")
    tree = parser.parse(code)
    Interpreter().transform(tree)



#   SAMPLE

if __name__ == "__main__":
    program = r"""
    SET a 10
    SET b 20
    yap "Start!"

    imo add(x, y):
        yap x + y
    END

    call add(a, b)

    kalo a < 15:
        yap a
        SET a a + 1
    END

    cmiiw i in 5:
        yap i
    END
    """
    run(program)
