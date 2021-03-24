from lexer import CalcLexer
from sly import Parser
from helpers import tcolours, constant_operands, expr_str
from symbol_table import ctx_stack
from errors import runtime_error


class ExpressionParser(Parser):
    tokens = CalcLexer.tokens
    start = 'eq_expression'

    # Error handler
    def error(self, err):
        if err:
            print(tcolours.red + "ERR" + tcolours.reset + " - " + "Line {}: ".format(err.lineno) + err.value)
        else:
            print(err)

    #
    # Expressions
    #

    @_('rel_expression')
    def eq_expression(self, p):
        return p[0]

    @_('rel_expression EQUALS eq_expression')
    def eq_expression(self, p):
        if constant_operands(p):
            return p[0] == p[2]
        else:
            return expr_str(p)

    # rel_expression

    @_('sum_expression')
    def rel_expression(self, p):
        return p[0]

    @_('sum_expression ">" rel_expression')
    def rel_expression(self, p):
        if constant_operands(p):
            return p[0] > p[2]
        else:
            return expr_str(p)

    @_('sum_expression "<" rel_expression')
    def rel_expression(self, p):
        if constant_operands(p):
            return p[0] < p[2]
        else:
            return expr_str(p)

    # sum_expression

    @_('mul_expression')
    def sum_expression(self, p):
        return p[0]

    @_('mul_expression "+" sum_expression')
    def sum_expression(self, p):
        if constant_operands(p):
            return p[0] + p[2]
        else:
            return expr_str(p)

    @_('mul_expression "-" sum_expression')
    def sum_expression(self, p):
        if constant_operands(p):
            return p[0] - p[2]
        else:
            return expr_str(p)

    # mul_expression

    @_('primary_expression')
    def mul_expression(self, p):
        return p[0]

    @_('primary_expression "*" mul_expression')
    def mul_expression(self, p):
        if constant_operands(p):
            return p[0] * p[2]
        else:
            return expr_str(p)

    @_('primary_expression "/" mul_expression')
    def mul_expression(self, p):
        if constant_operands(p):
            return p[0] / p[2]
        else:
            return expr_str(p)

    @_('primary_expression "%" mul_expression')
    def mul_expression(self, p):
        if constant_operands(p):
            return p[0] % p[2]
        else:
            return expr_str(p)

    @_('FLOAT')
    def primary_expression(self, p):
        return float(p[0])

    @_('INTEGER')
    def primary_expression(self, p):
        return int(p[0])

    @_('STRING')
    def primary_expression(self, p):
        return p[0]

    @_('"(" eq_expression ")"')
    def primary_expression(self, p):
        return p[1]

    @_('ID')
    def primary_expression(self, p):
        var = ctx_stack.search_variable(p[0])

        if var:
            if var.value:
                return var.value
            else:
                runtime_error("Can not assign to variable {} because it does not have a value".format(p[0]))
                # Runtime error. Variable does not have a value
        else:
            pass
            # Runtime error. Variable not declared


if __name__ == "__main__":
    lexer = CalcLexer()
    parser = ExpressionParser()
    text = '32 * (1+2)'

    print(parser.parse(lexer.tokenize(text)))
