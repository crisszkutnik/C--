from sly import Lexer

class CalcLexer(Lexer):
    tokens = {
        ID,
        FLOAT,
        INTEGER,
        STRING,

        # Operators
        EQUALS,

        # Keywords
        IF,
        ELIF,
        ELSE,
        WHILE,
        FOR,
        PLEASE,
        DEFINE,
        DO,
        LIST,

        #Data types
        INT,
        FLOAT_T,
        STRING_T,
        VOID
    }

    operators = {
        '+', '-', '/', '*', '=', '%', '>', '<'
    }

    other = {
        '(', ')', ';', '{', '}', '[', ']', ','
    }

    literals = operators | other

    # Set ignored tokens

    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Set regular expressions for each token
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    FLOAT = r'\d+\.\d+'
    INTEGER = r'\d+'
    #STRING = r'\"(^"[]|"\\\"")*\"'
    #STRING = r'\"([^\"]|(\\\")"*\"")"])"'
    #STRING = r'\"([^\"]|\")*\"'
    STRING = r'\"[^\"]*\"'

    # Operators
    EQUALS = r'=='

    # Keywords
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['please'] = PLEASE
    ID['do'] = DO
    ID['list'] = LIST

    #Data types
    ID['int'] = INT
    ID['float'] = FLOAT_T
    ID['string'] = STRING_T
    ID['void'] = VOID
    ID['elif'] = ELIF

    # Rule for newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    @_(INTEGER)
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(FLOAT)
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    def error(self, t):
        print("\nLine {}: Bad character {}\n".format(self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    data = '"abc""cde"'
    lexer = CalcLexer()

    for tok in lexer.tokenize(data):
        print(tok)
