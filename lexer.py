import ply.lex as lex


class IllegalCharacter(Exception):
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __str__(self):
        return repr("{}, line {}".format(self.value, self.line))


tokens = [
             'DOT',
             'DELIMITERL',
             'DELIMITERR',
             'CONJUNCTION',
             'DISJUNCTION',
             'ID',
             'CORKSCREW',
         ]


def t_ID(t):
    r'[a-z_A-Z][_\w]*'
    return t


t_DOT = r'\.'
t_CONJUNCTION = r','
t_DISJUNCTION = r';'
t_DELIMITERL = r'\('
t_DELIMITERR = r'\)'
t_CORKSCREW = r':-'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise IllegalCharacter(t.value[0], t.lineno)


def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()


def get_tokens(text):
    lexer.input(text)
    token_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_list.append(tok)
    return token_list
