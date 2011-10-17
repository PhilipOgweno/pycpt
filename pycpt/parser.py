import logging

import ply.yacc
import ply.lex

import lexer
import grammar

logger = logging.getLogger('pycpt.parser')

if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)

    cpt_lexer = ply.lex.lex(lexer)

    GMT_POLAR = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_polar.cpt'
    GMT_RELIEF = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_relief.cpt'
    GMT_RELIEF_MODIFIED = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_relief_modified.cpt'
    GMT_OCEAN = r'C:\Users\rjs\PycharmProjects\pycpt\cpt\GMT_ocean.cpt'

    with open(GMT_RELIEF_MODIFIED, 'r') as cpt_file:
        cpt_data = cpt_file.read()

    parser = ply.yacc.yacc(module=grammar, debug=True)
    parse_tree = parser.parse(cpt_data, lexer=cpt_lexer, debug=logger)
    pass

