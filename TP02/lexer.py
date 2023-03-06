import ply.lex as lex

tokens = ('ID_AREAS', 'ID_CONCEPT', 'ID_LANGS', 'ID_LANG', 'SEP', 'SEP2', 'SEP3',
          'GENDER', 'TYPE_TERM', 'ID_COUNTRY', 'WORDS')

literals = ['.', '(', ')', '*', '-', '|']


def t_ID_CONCEPT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID_AREAS(t):
    r'Areas'
    return t


def t_WORDS(t):
    r'\w+(\s\w+)*'
    return t


def t_ID_LANGS(t):
    r'Languages'
    return t


def t_ID_LANG(t):
    r'(ga|es|en|pt)'
    return t


def t_GENDER(t):
    r'\w'
    return t


def t_TYPE_TERM(t):
    r'\w+'
    return t


def t_ID_COUNTRY(t):
    r'\w+\.'
    return t


def t_SEP(t):
    r'\n\t'
    return t


def t_SEP2(t):
    r'\n\t\t'
    return t


def t_SEP3(t):
    r'\n\t\t\t'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' *'


def t_error(t):
    print(f'Illegal Character: {t.value[0]}.')
    t.lexer.skip(1)


lexer = lex.lex()
