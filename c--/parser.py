from lexer import CalcLexer
from sly import Parser
from helpers import tcolours, is_constant, constant_operands, expr_str, is_identifier
from symbol_table import ctx_stack, Variable
from errors import semantic_error
from nodes import AssignExpressionNode, DeclarationNode


def expression_is_parsed(expr: str):
    if is_identifier(expr):
        return False
    else:
        for e in CalcLexer.operators:
            if e in expr:
                return False


class CalcParser(Parser):
    tokens = CalcLexer.tokens
    start = 'declaration'

    # Error handler
    def error(self, err):
        if err:
            print(err)
            print(tcolours.red + "ERR" + tcolours.reset + " - " + "Line {}: ".format(err.lineno) + err.value)
        else:
            print(err)

    # Rules
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
        else:
            new_node = AssignExpressionNode(p[0], p[1], type(p[2]) is str if expression_is_parsed(p[2]) else True)
            return "{} = {}".format(p[1], p[2])

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
            if is_constant(p[1]):
                return p[1]
            else:
                return "({})".format(p[1])
        else:
            try:
                return int(p[0])
            except:
                try:
                    return float(p[0])
                except:  # Is another variable
                    var = ctx_stack.search_variable(p[0])

                    if var:
                        if var.is_parsed:
                            if var.value:
                                return var.value
                            else:
                                return p[0]  # Variable exists but does not have a value yet
                        else:
                            return p[0]  # Variable exists but it has not been completely parsed yet
                    else:
                        semantic_error("Variable {} is not declared".format(p[0]))

    #
    # Declarations
    #

    @_('declaration_specifiers opt_declaration')
    def declaration(self, p):
        data_type, identifier = p.declaration_specifiers
        is_parsed = True

        # If the string has an operator, it has not been completely parsed yet
        if type(p[1]) is str:
            is_parsed = expression_is_parsed(p[1])

        ctx_stack.context_add_instruction(
            DeclarationNode(identifier, p[1], data_type, is_parsed)
        )

        return p

    @_('PLEASE data_type ID')
    def declaration_specifiers(self, p):
        return p[1], p[2]

    @_('INT',
       'FLOAT_T',
       'STRING_T'
       )
    def data_type(self, p):
        if p[0] == "int":
            return int
        elif p[0] == "float":
            return float
        elif p[0] == "string":
            return str

    @_('";"',
       'initializer ";"'
       )
    def opt_declaration(self, p):
        if len(p) == 1:
            return None
        else:
            return p[0]

    @_('"=" eq_expression')
    def initializer(self, p):
        return p[1]


if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
    text = "please int a = 32 % (1 + 10);"
    # text = "please int a = abc;"

    # newvar = Variable("abc", int, True)
    # ctx_stack.variable_add_to_context(newvar)

    parser.parse(lexer.tokenize(text))
    # print(ctx_stack.stack[0].instructions[0].parsing_completed)
    ctx_stack.run_context()
    print(ctx_stack.variable_get_value("a"))

