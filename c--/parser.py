from lexer import CalcLexer
from sly import Parser
from helpers import tcolours
from symbol_table import symbol_table, Variable

class CalcParser(Parser):
    tokens = CalcLexer.tokens
    start = 'declaration'
   
    # Error handler
    def error(self, err): 
        if err:
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
       'eq_expression "=" assing_expression'
       )
    def assing_expression(self, p):
        return p

    @_('rel_expression',
       'rel_expression EQUALS eq_expression'
       )
    def eq_expression(self, p):
        return p

    @_('sum_expression',
       'sum_expression ">" rel_expression',
       'sum_expression "<" rel_expression'
       )
    def rel_expression(self, p):
        return p

    @_('mul_expression',
       'mul_expression "+" sum_expression',
       'mul_expression "-" sum_expression'
       )
    def sum_expression(self, p):
        return p

    @_('primary_expression',
       'primary_expression "*" mul_expression',
       'primary_expression "/" mul_expression',
       'primary_expression "%" mul_expression'
       )
    def mul_expression(self, p):
        return p

    @_('ID',
       'FLOAT',
       'INTEGER',
       'STRING',
       '"(" expression ")"'
       )
    def primary_expression(self, p):
        return p

    #
    # Declarations
    #

    @_('declaration_specifiers opt_declaration')
    def declaration(self, p):
        data_type, identifier = p.declaration_specifiers
        return p

    @_('PLEASE data_type ID')
    def declaration_specifiers(self, p):
        return p[1], p[2]

    @_('INT',
       'FLOAT_T',
       'STRING_T',
       'VOID'
       )
    def data_type(self, p):
        return p[0]

    @_('";"',
       'initializer ";"'
       )
    def opt_declaration(self, p): 
        return p

    @_('"=" expression')
    def initializer(self, p):
        return p

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
    text = "please int a;"

    parser.parse(lexer.tokenize(text))
