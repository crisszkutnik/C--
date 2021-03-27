from lexer import CalcLexer
from sly import Parser
from helpers import tcolours, is_constant, constant_operands, expr_str, is_identifier
from symbol_table import ctx_stack, BlockContext
from errors import semantic_error
from nodes import AssignExpressionNode, DeclarationNode, DecisionNode, ListDeclarationNode


def expression_is_parsed(expr: str):
    is_parsed = type(expr) is int or type(expr) is float or type(expr) is bool

    if not is_parsed:
        if is_identifier(expr):
            is_parsed = False
        else:
            for e in CalcLexer.operators:
                if e in expr:
                    is_parsed = False

    return is_parsed


def generate_block_context(instructions):
    new_context = BlockContext()
    new_context.instructions = instructions
    return new_context

class CalcParser(Parser):
    tokens = CalcLexer.tokens
    start = 'program'
    tmp_ctx = []

    # tmp_ctx is an auxiliary context used to parse statements

    # Error handler
    def error(self, err):
        if err:
            print(err)
            print(tcolours.red + "ERR: Syntax error" + tcolours.reset + " - Line {}: ".format(err.lineno) + err.value)
        else:
            print(tcolours.red + "ERR: Syntax error" + tcolours.reset + " - EOF")

    # Rules

    #
    # Expressions
    #

    @_('assign_expression')
    def expression(self, p):
        is_assign_expression, instruction = p[0]

        if is_assign_expression:
            ctx_stack.context_add_instruction(instruction)

        return p

    # assign_expresion

    @_('eq_expression')
    def assign_expression(self, p):
        return False, p[0]

    @_('ID "=" eq_expression')
    def assign_expression(self, p):
        is_parsed = type(p[2]) is int or type(p[2]) is float or type(p[2]) is bool

        if not is_parsed:
            is_parsed = expression_is_parsed(p[2])

        return True, AssignExpressionNode(p[0], p[2], is_parsed)

    # eq_expression

    @_('rel_expression')
    def eq_expression(self, p):
        return p[0]

    @_('rel_expression EQUALS eq_expression')
    def eq_expression(self, p):
        if constant_operands(p):
            return p[0] == p[2]
        else:
            return expr_str(p)

    # rel_expression

    @_('sum_expression')
    def rel_expression(self, p):
        return p[0]

    @_('sum_expression ">" rel_expression')
    def rel_expression(self, p):
        if constant_operands(p):
            return p[0] > p[2]
        else:
            return expr_str(p)

    @_('sum_expression "<" rel_expression')
    def rel_expression(self, p):
        if constant_operands(p):
            return p[0] < p[2]
        else:
            return expr_str(p)

    # sum_expression

    @_('mul_expression')
    def sum_expression(self, p):
        return p[0]

    @_('mul_expression "+" sum_expression')
    def sum_expression(self, p):
        if constant_operands(p):
            return p[0] + p[2]
        else:
            return expr_str(p)

    @_('mul_expression "-" sum_expression')
    def sum_expression(self, p):
        if constant_operands(p):
            return p[0] - p[2]
        else:
            return expr_str(p)

    # mul_expression

    @_('primary_expression')
    def mul_expression(self, p):
        return p[0]

    @_('primary_expression "*" mul_expression')
    def mul_expression(self, p):
        if constant_operands(p):
            return p[0] * p[2]
        else:
            return expr_str(p)

    @_('primary_expression "/" mul_expression')
    def mul_expression(self, p):
        if constant_operands(p):
            return p[0] / p[2]
        else:
            return expr_str(p)

    @_('primary_expression "%" mul_expression')
    def mul_expression(self, p):
        if constant_operands(p):
            return p[0] % p[2]
        else:
            return expr_str(p)

    # primary_expression

    @_('FLOAT')
    def primary_expression(self, p):
        return float(p[0])

    @_('INTEGER')
    def primary_expression(self, p):
        return int(p[0])

    @_('STRING')
    def primary_expression(self, p):
        return p[0]

    @_('ID arr_access')
    def primary_expression(self, p):
        var = ctx_stack.search_variable(p[0])

        if var:
            return p[0] + "[{}]".format(p[1]) if p[1] is not None else ""
        else:
            semantic_error("Variable {} is not declared".format(p[0]))

    @_('"(" eq_expression ")"')
    def primary_expression(self, p):
        if is_constant(p[1]):
            return p[1]
        else:
            return "({})".format(p[1])

    @_('"[" eq_expression "]"')
    def arr_access(self, p):
        return p[1]

    @_('empty')
    def arr_access(self, p):
        return None

    @_('eq_expression "," expression_list')
    def expression_list(self, p):

        return [(expression_is_parsed(p[0]), p[0])] + p[2]

    @_('eq_expression')
    def expression_list(self, p):
        return [(expression_is_parsed(p[0]), p[0])]

    #
    # Declarations
    #

    @_('PLEASE declaration2')
    def declaration(self, p):
        return p

    @_('var_declaration',
       'list_declaration'
       )
    def declaration2(self, p):
        return p

    @_('LIST ID opt_list_declaration')
    def list_declaration(self, p):
        node = ListDeclarationNode(p[1], p[2])
        node.add_to_context()
        ctx_stack.context_add_instruction(node)

        return p

    @_('";"')
    def opt_list_declaration(self, p):
        return None

    @_('"=" "[" expression_list "]" ";"')
    def opt_list_declaration(self, p):
        return p[2]

    @_('declaration_specifiers opt_declaration')
    def var_declaration(self, p):
        data_type, identifier = p.declaration_specifiers

        is_parsed = expression_is_parsed(p[1])

        node = DeclarationNode(identifier, p[1], data_type, is_parsed)

        node.add_to_context()
        ctx_stack.context_add_instruction(node)

        return p

    @_('data_type ID')
    def declaration_specifiers(self, p):
        return p[0], p[1]

    # data_type

    @_('INT')
    def data_type(self, p):
        return int

    @_('FLOAT_T')
    def data_type(self, p):
        return float

    @_('STRING_T')
    def data_type(self, p):
        return str

    # opt_declaration

    @_('";"')
    def opt_declaration(self, p):
        return None

    @_('initializer ";"')
    def opt_declaration(self, p):
        return p[0]

    # initializer

    @_('"=" eq_expression')
    def initializer(self, p):
        return p[1]

    #
    # Sentences
    #

    @_('compound_sentence',
       'decision_sentence'
       )
    def sentence(self, p):
        return p

    @_('"{" "{" push_block_context code_block_list "}" "}"')
    def compound_sentence(self, p):
        ctx = p[2]
        return ctx_stack.pop_context()

    @_('PLEASE IF "(" eq_expression ")" DO compound_sentence else_statement')
    def decision_sentence(self, p):
        ctx_stack.context_add_instruction(
            DecisionNode([(p[3], p[6])] + p[7])
        )
        return p

    @_('empty')
    def else_statement(self, p):
        return []

    @_('ELSE DO compound_sentence')
    def else_statement(self, p):
        return [(None, p[2])]

    @_('ELIF "(" eq_expression ")" DO compound_sentence else_statement')
    def else_statement(self, p):
        return [(p[2], p[5])] + p[6]

    #
    # Code structure
    #

    @_('code_block_list')
    def program(self, p):
        return p

    @_('code_block code_block_list',
       'empty'
       )
    def code_block_list(self, p):
        return p

    @_('declaration')
    def code_block(self, p):
        return p

    @_('expression ";"')
    def code_block(self, p):
        return p

    @_('sentence')
    def code_block(self, p):
        return p

    #
    # Misc
    #

    @_('')
    def empty(self, p):
        pass

    @_('')
    def push_block_context(self, p):
        ctx = BlockContext()
        ctx_stack.add_context(ctx)
        return ctx

if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
    # text = "please int a = 32 % (1 + 10); please int b = a;"
    # text = "please int a; please int abc = a"
    # text = "please int a = 10; please int b = a * 2;"
    # text = "please int a = 10; please int b = (a - 5) * 3;"
    # text = "please int a = 10; a = 5;"
    text = """
            please int b = 5;
            please list a = [1, 2, b * 2, 4, 5];
            """

    parser.parse(lexer.tokenize(text))

    # ctx_stack.run_context()
    # print(ctx_stack.variable_get_value("abc"))
    # print(ctx_stack.variable_get_value("a"))
