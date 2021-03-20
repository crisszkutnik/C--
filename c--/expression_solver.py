from lexer import CalcLexer
from sly import Parser
from helpers import tcolours

def is_constant(arg):
    arg_t = type(arg)
    return (arg_t is int or arg_t is float)

def expr_str(p):
    return "{}{}{}".format(p[0], p[1], p[2])

def constant_operands(p):
    return (is_constant(p[0]) and is_constant(p[2]))

class ExpressionParser(Parser):
    tokens = CalcLexer.tokens
    start = 'expression'

    # Error handler
    def error(self, err): 
        if err:
            print(tcolours.red + "ERR" + tcolours.reset + " - " + "Line {}: ".format(err.lineno) + err.value)
        else:
            print(err)

    #
    # Expressions
    #

    @_('assing_expression')
    def expression(self, p):
        return p

    @_('eq_expression',
       'eq_expression "=" assing_expression'
       )
    def assing_expression(self, p):
        print(p[0])
        return p

    @_('rel_expression',
       'rel_expression EQUALS eq_expression'
       )
    def eq_expression(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            if constant_operands(p):
                return p[0] == p[2]
            else:
                return expr_str(p)

    @_('sum_expression',
       'sum_expression ">" rel_expression',
       'sum_expression "<" rel_expression'
       )
    def rel_expression(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            if constant_operands(p):
                if p[1] == ">":
                    return p[0] > p[2]
                elif p[1] == "<":
                    return p[0] < p[2]
            else:
                return expr_str(p)
            

    @_('mul_expression',
       'mul_expression "+" sum_expression',
       'mul_expression "-" sum_expression'
       )
    def sum_expression(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            if constant_operands(p):
                if p[1] == "+":
                    return p[0] + p[2]
                elif p[1] == "-":
                    return p[0] - p[2]
            else:
                return expr_str(p)


    @_('primary_expression',
       'primary_expression "*" mul_expression',
       'primary_expression "/" mul_expression',
       'primary_expression "%" mul_expression'
       )
    def mul_expression(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            if constant_operands(p):
                if p[1] == "*":
                    return p[0] * p[2]
                elif p[1] == "/":
                    return p[0] / p[2]
                elif p[1] == "%":
                    return p[0] % p[2]
            else:
                return expr_str(p)


    @_('ID',
       'FLOAT',
       'INTEGER',
       'STRING',
       '"(" expression ")"'
       )
    def primary_expression(self, p):
        try:
            return int(p[0])
        except:
            try:
                return float(p[0])
            except:
                return p[0]

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = ExpressionParser()
    text = "5 * 2 + 10 / 2"

    parser.parse(lexer.tokenize(text))
