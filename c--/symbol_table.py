from errors import semantic_error


class Variable:
    def __init__(self, name, t, value=None):
        self.name = name
        self.type = t
        self.value = value

    def modify_value(self, new_value):
        if self.type == type(new_value):
            self.value = new_value
        else:
            semantic_error("types do not match")


class InstructionContext:
    variables = []
    contexts = []
    instructions = []

    def add_variable(self, var):
        self.variables.append(var)

    def add_instruction(self, ins):
        self.instructions.append(ins)

    def add_context(self, ctx):
        self.contexts.append(ctx)


class FunctionContext(InstructionContext):
    def __init__(self, name, t, args=[]):
        self.name = name
        self.return_type = t
        self.args = args

    def run(self):
        for i in self.instructions:
            i.run_instruction()


class BlockContext(InstructionContext):
    def __init__(self, node):
        self.node = node

    def run(self):
        self.node.run_node()


class ContextStack:
    def __init__(self):
        self.stack = [FunctionContext('main', 'void')]

    def search_variable(self, name):
        for i in range(len(self.stack) - 1, -1, -1):
            variables = self.stack[i].variables
            for var in variables:
                if var.name == name:
                    return var

        return None

    def stack_head(self):
        return self.stack[-1]

    #
    # Variable methods on context
    #

    def variable_is_declared(self, name: str) -> bool:
        return not (self.search_variable(name) is None)

    def variable_get_value(self, name: str):
        var = self.search_variable(name)
        if not (var is None):
            return var.value
        else:
            semantic_error("variable {} is not declared".format(name))
            # Raise error. Variable not declared

    def variable_add_to_context(self, var: Variable):
        self.stack_head().add_variable(var)

    def variable_modify_value(self, name: str, new_value):
        var = self.search_variable(name)

        if not (var is None):
            var.modify_value(new_value)
        else:
            semantic_error("variable {} is not declared".format(name))
            # Raise error. Variable not declared

    #
    # Context management methods
    #

    def add_context(self, new_ctx):
        head = self.stack_head()
        head.add_context(new_ctx)
        self.stack.append(new_ctx)

    def pop_context(self):
        self.stack.pop()

    def context_add_instruction(self, ins):
        self.stack_head().add_instruction(ins)

    def run_context(self):
        for ctx in self.stack:
            ctx.run()


ctx_stack = ContextStack()
