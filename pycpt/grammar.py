'''
A grammar for CPT files
'''
import logging

from pycpt.ast import (CommentNode, ColorModelNode, IntervalSpecNode,
                       TripletNode, CMYKColorNode, GrayColorNode, RGBColorNode,
                       NamedColorNode, CategoryNode)

logger = logging.getLogger('pycpt.grammar')

# Get the token map from the lexer.  This is required.
from lexer import tokens

def p_cpt(p):
    '''
    cpt : statement_list
    '''
    p[0] = p[1]

def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

def p_statement(p):
    '''
    statement : comment_statement EOL
              | color_model_statement EOL
              | interval_statement EOL
              | category_statement EOL
    '''
    p[0] = p[1]

def p_comment_statement(p):
    '''comment_statement : COMMENT'''
    p[0] = CommentNode(p[1])

def p_color_model_statement(p):
    '''color_model_statement : COLOR_MODEL'''
    p[0] = ColorModelNode(p[1][0], p[1][1])

def p_interval_statement(p):
    '''interval_statement : interval_spec
                          | annotated_interval_spec
                          | labelled_interval_spec
                          | annotated_and_labelled_interval_spec
    '''
    p[0] = p[1]

def p_category_statement(p):
    '''category_statement : CODE triplet
                          | CODE hexrgb
                          | CODE x11
                          | CODE gray
                          | CODE cmyk
    '''
    p[0] = CategoryNode(p[1], p[2])

'''
                  | FLOAT cmyk FLOAT cmyk
                  | FLOAT cmyk FLOAT hexrgb
                  | FLOAT cmyk FLOAT x11

                  | FLOAT gray FLOAT gray
                  | FLOAT gray FLOAT hexrgb
                  | FLOAT gray FLOAT x11
                  | FLOAT hexrgb FLOAT triplet
                  | FLOAT hexrgb FLOAT cmyk
                  | FLOAT hexrgb FLOAT hexrgb
                  | FLOAT hexrgb FLOAT x11

                  | FLOAT x11 FLOAT cmyk
                  | FLOAT x11 FLOAT hexrgb
                  | FLOAT x11 FLOAT x11
'''

def p_interval_spec(p):
    '''
    interval_spec : FLOAT triplet FLOAT triplet
                  | FLOAT hexrgb FLOAT triplet
                  | FLOAT triplet FLOAT hexrgb
                  | FLOAT x11 FLOAT triplet
                  | FLOAT triplet FLOAT x11
    '''
    p[0] = IntervalSpecNode(p[1], p[2], p[3], p[4])

def p_annotated_interval_spec(p):
    '''
    annotated_interval_spec : interval_spec CODE
    '''
    p[1].annotation = p[2]
    p[0] = p[1]

def p_labelled_interval_spec(p):
    '''
    labelled_interval_spec : interval_spec LABEL
    '''
    p[1].label = p[2]
    p[0] = p[1]

def p_annotated_and_labelled_interval_spec(p):
    '''
    annotated_and_labelled_interval_spec : interval_spec CODE LABEL
    '''
    p[1].annotation = p[2]
    p[1].label = p[3]
    p[0] = p[1]

def p_triplet(p):
    '''
    triplet : FLOAT FLOAT FLOAT
    '''
    p[0] = TripletNode(p[1], p[2], p[3])

def p_cmyk(p):
    '''
    cmyk : FLOAT FLOAT FLOAT FLOAT
    '''
    p[0] = CMYKColorNode(p[1], p[2], p[3], p[4])

def p_gray(p):
    '''
    gray : FLOAT
    '''
    p[0] = GrayColorNode(p[1])

def p_hexrgb(p):
    '''
    hexrgb : HEXTRIPLE
    '''
    p[0] = RGBColorNode(int(p[1][0:2], 16),
                        int(p[1][2:4], 16),
                        int(p[1][4:6], 16))

def p_x11(p):
    '''
    x11 : NAME
    '''
    p[0] = NamedColorNode(p[1])

def p_error(p):
    logger.error("Syntax error {0} at line {1}".format(p, p.lineno))
