import logging
import re


import ply.lex as lex

logger = logging.getLogger('cpt.lexer')

tokens = ('COLOR_MODEL', 'EOL', 'COMMENT', 'HEXTRIPLE', 'FLOAT',
          'CODE', 'LABEL', 'NAME')

def t_EOL(t):
    r'(\n|\r\n?)'
    t.lexer.lineno += 1
    return t

def t_COLOR_MODEL(t):
    r'\#\s*COLOU?R_MODEL\s*=\s*(\+?)\s*(RGB|HSV|CMYK)'
    m = re.match(t_COLOR_MODEL.__doc__, t.value)
    t.value = (m.group(1), m.group(2))
    return t

def t_HEXTRIPLE(t):
    r'\#([0-9A-Fa-f]{6})\b'
    m = re.match(t_HEXTRIPLE.__doc__, t.value)
    t.value = m.group(1)
    return t

def t_COMMENT(t):
    r'\#([^\n]*)'
    m = re.match(t_COMMENT.__doc__, t.value)
    t.value = m.group(1)
    return t

def t_FLOAT(t):
    r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    t.value = float(t.value)
    return t

def t_NAME(t):
    r'[A-Za-z]{2,}\w*'
    return t

def t_CODE(t):
    r'\b[FNLUB]\b'
    return t

def t_LABEL(t):
    r';\s*(.+)'
    m = re.match(t_LABEL.__doc__, t.value)
    t.value = m.group(1)
    return t

t_ignore = ' \t'

def t_error(t):
    logger.error("Illegal character {0}".format(t.value[0]))
    t.lexer.skip(1)

if __name__ == '__main__':
    GMT_POLAR = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_polar.cpt'
    GMT_RELIEF = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_relief.cpt'
    GMT_RELIEF_MODIFIED = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_relief_modified.cpt'
    GMT_OCEAN = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_ocean.cpt'

    with open(GMT_RELIEF_MODIFIED, 'r') as cpt_file:
        cpt_data = cpt_file.read()

    #cpt_lines = cpt_data.splitlines()

    # Build the lexer
    lexer = lex.lex()

    lexer.input(cpt_data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

#    for lineno, line in enumerate(cpt_lines):
#        # Give the lexer some input
#        lexer.input(line)
#        # Tokenize
#        while True:
#            tok = lexer.token()
#            if not tok: break      # No more input
#            tok.lineno = lineno
#            print tok
#        eol = lex.LexToken()
#        eol.type = 'EOL'
#        eol.value = '\n'
#        eol.lineno = lineno
#        eol.lexpos = len(line)
#        print eol