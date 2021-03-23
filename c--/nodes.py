from symbol_table import ctx_stack, Variable
from errors import semantic_error
from helpers import is_constant


#
# Expressions
#

class AssignExpressionNode:
    def __init__(self, operator, expr, parsing_completed):
        self.operator = operator
        self.expr = expr
        self.parsing_completed = parsing_completed

    def run_instruction(self):
        var = ctx_stack.search_variable(self.operator)

        if var:
            if self.parsing_completed:
                var.value = self.expr
            else:
                # Parse the expression again and assign the value
                pass
        else:
            pass
            # Runtime error. Variable not declared


#
# Declarations
#

class DeclarationNode:
    def __init__(self, identifier, expr, t, parsing_completed):
        self.identifier = identifier
        self.expr = expr
        self.t = t
        self.parsing_completed = parsing_completed

    def run_instruction(self):
        if ctx_stack.variable_is_declared(self.identifier):
            # Raise error. Variable already declared
            pass
        else:
            if not self.parsing_completed:
                pass
                # Parse expr again

            ctx_stack.variable_add_to_context(Variable(self.identifier, self.t, self.parsing_completed, self.expr))
