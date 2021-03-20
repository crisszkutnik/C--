class variable:
    def __init__(self, name, t, value=None):
        self.name = name
        self.t = t
        self.value = value

class instruction_context:
    variables = []
    contexts = []
    instructions = []

    def add_variable(self, var):
        self.instructions.append(var)

    def add_instruction(self, ins):
        self.instructions.append(ins)

    def add_context(self, ctx):
        self.contexts.append(ctx)

    def run(self):
        for i in instructions:
            i.run_instruction()

class function_context(instruction_context):
    def __init__(self, name, t, args=[]):
        self.name = name
        self.return_type = t
        self.args = args

class block_context(instruction_context):
    def __init__(self):
        pass

class context_stack:
    def __init__(self):
        self.stack = [function_context(main, 'void')]

    def search_variable(self, name):
        for i in range(len(stack) - 1, -1, -1):
            variables = stack[i].variables
            for var in variables:
                if(var.name == name):
                    return var

        return None

    def stack_head(self):
        return self.stack[-1]

    #
    # Variable methods on context
    #
        
    def variable_is_declared(self, name):
        return self.search_variable(name) != None

    def variable_get_value(self, name):
        var = self.search_variable(name)
        return var.value
    
    def variable_add_to_context(self, var):
        self.stack_head().add_variable(var)

    #
    # Context managment methods
    #

    def add_context(self, new_ctx):
        head = self.stack_head()
        head.add_context(new_ctx)
        self.stack.append(new_ctx)

    def pop_context(self):
        self.stack.pop()

ctx_stack = context_stack()
