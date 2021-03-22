from lexer import CalcLexer
from sly import Parser
from helpers import tcolours, is_constant, constant_operands, expr_str
from symbol_table import ctx_stack, variable

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
        if(len(p) == 1):
            return p[0]
        elif ctx_stack.variable_is_declared(p[0]):
            if is_constant(p[2]) or p[2][0] == '"':
                ctx_stack.variable_modify_value(p[0], p[2])
            elif ctx_stack.variable_is_declared(p[2]): # Assign to another variable
                new_val = ctx_stack.variable_get_value(p[2])
                ctx_stack.variable_modify_value(new_val)
            else:
                pass
                # Raise error. Variable on p[2] is not declared

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
                    return p[0]

    #
    # Declarations
    #

    @_('declaration_specifiers opt_declaration')
    def declaration(self, p):
        data_type, identifier = p.declaration_specifiers
        
        if not ctx_stack.variable_is_declared(identifier):
            var_type = type(p[1])
            if var_type is None or var_type is data_type:
                ctx_stack.variable_add_to_context(variable(identifier, data_type, p[1]))
            else:
                pass
                # Raise error. Declaration type and assigned type do not match
        else:
            pass
            # Raise error. Variable already declared

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
        if(len(p) == 1):
            return None
        else:
            return p[0]

    @_('"=" eq_expression')
    def initializer(self, p):
        return p[1]

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
    text = "please int a = 32 * (1 + 2);"

    parser.parse(lexer.tokenize(text))
    print(ctx_stack.variable_get_value("a"))
