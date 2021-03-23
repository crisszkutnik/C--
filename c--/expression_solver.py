from lexer import CalcLexer
from sly import Parser
from helpers import tcolours, constant_operands, expr_str, is_constant
from symbol_table import ctx_stack, Variable
from errors import semantic_error


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
       'ID "=" eq_expression'
       )
    def assing_expression(self, p):
        if len(p) == 1:
            return p[0]
        elif ctx_stack.variable_is_declared(p[0]):
            if is_constant(p[2]) or p[2][0] == '"':
                ctx_stack.variable_modify_value(p[0], p[2])
            elif ctx_stack.variable_is_declared(p[2]):  # Assign to another variable
                new_val = ctx_stack.variable_get_value(p[2])
                ctx_stack.variable_modify_value(new_val)
            else:
                semantic_error("Variable {} is not declared".format(p[2]))
                # Raise error. Variable on p[2] is not declared

    @_('rel_expression',
       'rel_expression EQUALS eq_expression'
       )
    def eq_expression(self, p):
        if len(p) == 1:
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
        if len(p) == 1:
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
        if len(p) == 1:
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
        if len(p) == 1:
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
       '"(" eq_expression ")"'
       )
    def primary_expression(self, p):
        if p[0] == "(":
            return p[1]
        else:
            try:
                return int(p[0])
            except:
                try:
                    return float(p[0])
                except:
                    val = ctx_stack.variable_get_value(p[0])

                    if val:
                        return val
                    else:
                        return p[0]





if __name__ == "__main__":
    lexer = CalcLexer()
    parser = ExpressionParser()
    text = '32 * (1+2)'

    print(parser.parse(lexer.tokenize(text)))
