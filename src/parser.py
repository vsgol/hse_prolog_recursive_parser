from src.lexer import get_tokens


def lexer(s):
    for c in s:
        yield c
    while True:
        yield '\0'


class IncompleteToken(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(''.format(self.value))


class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name

    def __str__(self):
        a = "("
        if self.left is not None:
            a += self.left.__str__()
        a += " " + self.name + " "
        if self.right is not None:
            a += self.right.__str__()
        a += ')'
        return a


class Parser:
    def __init__(self, s):
        self.lex = lexer(s)
        self.current = next(self.lex)
        self.last = None

    def accept(self, c):
        if self.current == '\0':
            return False

        if self.current.type == c:
            self.last = self.current
            self.current = next(self.lex)
            return True
        return False

    def id(self):
        if self.current == '\0':
            return 0
        l = self.current
        self.last = l
        self.current = next(self.lex)
        if l.type != 'ID':
            return None
        return Node(None, None, l.value)

    def disj(self):
        l = self.conj()
        if self.accept('DISJUNCTION'):
            r = self.disj()
            if r is None:
                return None
            return Node(l, r, ";")
        return l

    def conj(self):
        l = self.lit()
        if self.accept('CONJUNCTION'):
            r = self.conj()
            if r is None:
                return None
            return Node(l, r, ",")
        return l

    def corkscrew(self):
        if self.accept('CORKSCREW'):
            r = self.disj()
            if r is None:
                return None
            return r

    def lit(self):
        if self.current == '\0':
            return None
        l = self.current
        if self.accept('DELIMITERL'):
            r = self.disj()
            if self.accept('DELIMITERR'):
                return r
            return None
        self.last = self.current
        self.current = next(self.lex)

        if l.type != 'ID':
            return None
        return Node(None, None, l.value)

    def attitude(self):
        l = self.id()
        if l == 0:
            return None
        if l is None:
            raise IncompleteToken("at line {}".format(self.last.lineno))
        if self.accept('DOT'):
            return self.last

        r = self.corkscrew()
        if r is None or not self.accept('DOT'):
            raise IncompleteToken("at line {}".format(self.last.lineno+1))
        return Node(l, r, ':-')


def parse(text):
    token_list = get_tokens(text)
    p = Parser(token_list)
    while True:
        tree = p.attitude()
        if tree is None:
            return True
