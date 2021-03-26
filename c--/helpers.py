import re
from lexer import CalcLexer


class tcolours:
    reset = "\033[0m"
    underline = "\033[4m"
    bold = "\033[1m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"


#
# Expression parser helpers
#

def is_constant(arg):
    arg_t = type(arg)
    return arg_t is int or arg_t is float


def expr_str(p):
    return "{}{}{}".format(p[0], p[1], p[2])


def constant_operands(p):
    return is_constant(p[0]) and is_constant(p[2])


def is_identifier(s: str):
    return re.search(CalcLexer.ID, s).group() == s


#
# Other
#

def is_truthy(expr):
    return expr or expr != 0
