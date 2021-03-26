from symbol_table import ctx_stack, Variable
from errors import semantic_error
from expression_solver import ExpressionParser
from lexer import CalcLexer
from helpers import is_truthy

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
        else:
            pass
            # Runtime error. Variable not declared


#
# Declarations
#

class DeclarationNode:
    def __init__(self, identifier, expr, t, is_parsed):
        self.identifier = identifier
        self.expr = expr
        self.t = t
        self.is_parsed = is_parsed
        self.var = Variable(self.identifier, self.t)

    # Adds variable to context that is on top of stack
    def add_to_context(self):
        if ctx_stack.variable_is_declared(self.identifier):
            semantic_error("Variable {} is already declared".format(self.identifier))
        else:
            ctx_stack.variable_add_to_context(self.var)

    def run_instruction(self):
        if self.is_parsed:
            self.var.value = self.expr
        else:
            self.var.value = parse_expr(self.expr)


#
# Sentences
#

# cases is of the shape [(expr, [instructions]]

class DecisionNode:
    def __init__(self, cases):
        self.cases = cases

    def run_instruction(self):
        for case in self.cases:
            expr, context = case

            if expr is None or is_truthy(parse_expr(expr)):
                ctx_stack.add_context(context)
                context.run()
                ctx_stack.pop_context()
                return
