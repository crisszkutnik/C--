from symbol_table import ctx_stack, Variable
from errors import semantic_error
from expression_solver import ExpressionParser
from lexer import CalcLexer

expression_parser = ExpressionParser()
expression_lexer = CalcLexer()


#
# Expressions
#

# Parse expr again
def parse_expr(expr):
    return expression_parser.parse(expression_lexer.tokenize(expr))


class AssignExpressionNode:
    def __init__(self, operator, expr, parsing_completed):
        self.operator = operator
        self.expr = expr
        self.parsing_completed = parsing_completed

    def run_instruction(self):
        var = ctx_stack.search_variable(self.operator)

        if var:
            if self.parsing_completed:
                var.modify_value(self.expr)
            else:
                new_val = parse_expr(self.expr)
                if new_val:
                    var.modify_value(new_val)
                pass
        else:
            pass
            # Runtime error. Variable not declared


#
# Declarations
#

class DeclarationNode:
    def __init__(self, identifier, expr, t):
        self.identifier = identifier
        self.expr = expr
        self.t = t
        self.var = Variable(self.identifier, self.t)

        if ctx_stack.variable_is_declared(self.identifier):
            semantic_error("Variable {} is already declared".format(identifier))
        else:
            ctx_stack.variable_add_to_context(self.var)

    def run_instruction(self):
        # ctx_stack.variable_add_to_context(Variable(self.identifier, self.t, parse_expr(self.expr)))
        self.var.value = parse_expr(self.expr)
