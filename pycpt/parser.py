'''
A parser for CPT files
'''

import re
import ply.lex as lex

tokens = ('COLOR_MODEL', 'COMMENT', 'HEXTRIPLE', 'FLOAT',
          'ANNOTATION', 'LABEL', 'SEMICOLON',
          'BACKGROUND', 'FOREGROUND', 'NAN', 'PLUS', 'HASH', 'CATEGORY', 'NAME')

def t_COLOR_MODEL(t):
    r'\#\s*COLOU?R_MODEL\s*=\s*(\+?)\s*(RGB|HSV|CMYK)'
    m = re.match(t_COLOR_MODEL.__doc__, t.value)
    t.value = (m.group(1), m.group(2))
    return t

def t_HEXTRIPLE(t):
    r'\#([0-9A-Fa-f]{6})(\s+|$)'
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

def t_CATEGORY(t):
    r'^([FBN])\s+'
    m = re.match(t_CATEGORY.__doc__, t.value)
    t.value = m.group(1)
    return t

def t_ANNOTATION(t):
    r'[LUB]'
    return t

def t_NAME(t):
    r'[A-Za-z]{2,}\w*'
    return t

def t_LABEL(t):
    r';\s*(.+)$'
    m = re.match(t_LABEL.__doc__, t.value)
    t.value = m.group(1)
    return t

t_SEMICOLON = ';'
t_BACKGROUND = 'B'
t_FOREGROUND = 'F'
t_NAN = 'N'
t_PLUS = '\+'
t_HASH = '\#'

t_ignore = ' \t'

def t_error(t):
    print "Illegal character {0}".format(t.value[0])
    t.lexer.skip(1)

def p_statement(p):
    '''statement : comment
                 | color_model_statement,
                 | interval_statement,
                 | category_statement'''
    p[0] = p[1]

def p_comment(p):
    p[0] = p[1]

def p_color_model_statement(p):
    '''

    color_model : COLOR_MODEL COLOR_SPACE
                | COLOR_MODEL PLUS COLOR_SPACE
    '''
    if len(p) == 3:
        p[0] = ColorModel(p[2])
    elif len(p) == 4:
        p[0] = ColorModel(p[2], interpolation=p[2])

def p_interval(p):
    '''interval : interval_spec
                | interval_spec ANNOTATION
                | interval_spec SEMICOLON LABEL
                | interval_spec ANNOTATION SEMICOLON LABEL
    '''
    if len(p) == 2:
        p[0] = IntervalNode(p[1])
    elif len(p) == 3:
        p[0] = IntervalNode(p[1], annotation=p[2])
    elif len(p) == 4:
        p[0] = IntervalNode(p[1], label=p[3])
    elif len(p) == 5:
        p[0] = IntervalNode(p[1], annotation=p[2], label=p[4])


def p_interval_spec(p):
    '''
    interval_spec : FLOAT triplet FLOAT triplet
                       | FLOAT triplet FLOAT hexrgb
                       | FLOAT triplet FLOAT x11
                       | FLOAT quad FLOAT quad
                       | FLOAT quad FLOAT hexrgb
                       | FLOAT quad FLOAT x11
                       | FLOAT gray FLOAT gray
                       | FLOAT gray FLOAT hexrgb
                       | FLOAT gray FLOAT x11
                       | FLOAT hexrgb FLOAT triplet
                       | FLOAT hexrgb FLOAT quad
                       | FLOAT hexrgb FLOAT hexrgb
                       | FLOAT hexrgb FLOAt x11
                       | FLOAT x11 FLOAT triplet
                       | FLOAT x11 FLOAT quad
                       | FLOAT x11 FLOAT hexrgb
                       | FLOAT x11 FLOAT x11
    '''
    p[0] = IntervalSpecNode(p[1], p[2], p[3], p[4])


def p_triplet(p):
    '''
    triplet : FLOAT FLOAT FLOAT
    '''
    p[0] = Triplet(p[1], p[2], p[3])

def p_cmyk(p):
    '''
    cmyk : FLOAT FLOAT FLOAT FLOAT
    '''
    p[0] = Quad(p[1], p[2], p[3], p[4])

def p_gray(p):
    '''
    gray : FLOAT
    '''
    p[0] = RGBColor(p[1], p[1], p[1])

def p_hexrgb(p):
    '''
    hexrgb : HEXRGB
    '''
    # TODO

def p_x11(p):
    '''
    x11 : WORD
    '''
    p[0] = X11Color(p[1])

GMT_POLAR = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_polar.cpt'
GMT_RELIEF = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_relief.cpt'
GMT_RELIEF_MODIFIED = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_relief_modified.cpt'
GMT_OCEAN = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_ocean.cpt'

with open(GMT_RELIEF_MODIFIED, 'r') as cpt_file:
    cpt_data = cpt_file.read()

cpt_lines = cpt_data.splitlines()

# Build the lexer
lexer = lex.lex()

for lineno, line in enumerate(cpt_lines):
    # Give the lexer some input
    lexer.input(line)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        tok.lineno = lineno
        print tok
    eol = lex.LexToken()
    eol.type = 'EOL'
    eol.value = '\n'
    eol.lineno = lineno
    eol.lexpos = len(line)
    print eol
