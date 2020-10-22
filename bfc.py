#!/usr/bin/env python3
''' bfc
Brainfsck Compiler
 
Written in Python3 using rply, which is a Python based parser/lexer with syntax similar to YACC.
'''

__author__ = "iivlx - iivlx@iivlx.com"
__date__ = (7,10,2019) #d,m,y
__version__ = (0,0,1) #0.0.1

from bfclex import Lexer
from bfcparse import Parser
from bfcg import BFCodeGenerator

def main():
    ''' Enter the filename of the code to be compiled...''' # sponge
    code = ''''''
    
    filename = input("bfc>")
    
    with open(filename, 'r') as file:
        code = file.read()
    
    lexer = Lexer().buildLexer()
    parser_generator = Parser()
    parser_generator.parse()
    parser = parser_generator.buildParser()
    
    code_generator = BFCodeGenerator()
    
    print("================ TOKENS ================")
    for token in lexer.lex(code):
        print(token)
    
    print("================ PARSED ================")
    tokens = lexer.lex(code)
    parsed = parser.parse(tokens, state=code_generator)
    print(parsed)
    
    print("================ EVAL ================")
    
    for e in parsed:
        e.eval()
    
    print(code_generator.variables)
    print(code_generator.code)
    
if __name__=='__main__':
    main()