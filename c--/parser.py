from lexer import CalcLexer
from sly import Parser
from helpers import tcolours

class CalcParser(Parser):
    tokens = CalcLexer.tokens
   
    # Error handler
    def error(self, err): 
        if err:
            print(tcolours.red + "ERR" + tcolours.reset + " - " + "Line {}: ".format(err.lineno) + err.value)
        else:
            print("Error at EOF")

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

    # Declarations

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
    text = "(a + 5) * 2"

    parser.parse(lexer.tokenize(text))
