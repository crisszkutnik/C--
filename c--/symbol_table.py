from errors import semantic_error


class VariableType:
    pass


class Variable(VariableType):
    def __init__(self, name, t, value=None):
        self.name = name
        self.type = t
        self.value = value

    def modify_value(self, new_value):
        if self.type == type(new_value):
            self.value = new_value
        else:
            semantic_error("types do not match")


class List(VariableType):
    def __init__(self, name, values=None):
        self.name = name
        self.value = values


class BlockContext:
    def __init__(self):
        self.variables = []
        self.contexts = []
        self.instructions = []

    def add_variable(self, var):
        self.variables.append(var)

    def add_instruction(self, ins):
        self.instructions.append(ins)

    def add_context(self, ctx):
        self.contexts.append(ctx)

    def run(self):
        for i in self.instructions:
            i.run_instruction()


# The context of a function is similar to a BlockContext but with extra features
class FunctionContext(BlockContext):
    def __init__(self, name, t, args=[]):
        super().__init__()
        self.name = name
        self.return_type = t
        self.args = args

    def run(self):
        for i in self.instructions:
            i.run_instruction()


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
        self.stack.append(new_ctx)

    def add_function_context(self, new_ctx):
        self.stack_head().add_context(new_ctx)
        self.add_context(new_ctx)

    def pop_context(self):
        return self.stack.pop()

    def context_add_instruction(self, ins):
        self.stack_head().add_instruction(ins)

    def run_context(self):
        for ctx in self.stack:
            ctx.run()


ctx_stack = ContextStack()
