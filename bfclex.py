#!/usr/bin/env python3

''' bfc
This is the lexer for bfc. It is used to tokenize the source file.
'''

from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
            
    def _add_tokens(self):
        ''' Create list of valid tokens. '''
        # comments
        self.lexer.add('COMMENT', r'//\s+.+\s+//')
              
        # numbers and math
        self.lexer.add('PLUSEQUALS', r'\+=')
        self.lexer.add('MINUSEQUALS', r'\-=')
        
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'\-')
        self.lexer.add('MULTIPLY', r'\*')
        self.lexer.add('DIVIDE', r'\/')
        self.lexer.add('EQUALS', r'\=')
        
        # keywords
        self.lexer.add('VAR', r'var')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('ENDIF', r'endif')
        self.lexer.add('END', r'end')
        self.lexer.add('PRINTNUM', r'printnum')
        self.lexer.add('PRINTINT', r'printint')
        self.lexer.add('PRINT', r'print')
        self.lexer.add('READASCII', r'read')
        self.lexer.add('ASCIITOINT', r'asciitoint')
        self.lexer.add('INTTOASCII', r'inttoascii')
        self.lexer.add('READINT', r'readint')
        self.lexer.add('ADD', r'add')
        self.lexer.add('COPY', r'copy')
        
        # debug
        self.lexer.add('TRACE', r'trace')
        
        # special characters
        self.lexer.add('SEMICOLON', r'\;')
        self.lexer.add('COLON', r'\:')
        
        # text
        self.lexer.add('NOP', r'nop')
        self.lexer.add('IDENTIFIER', r'\w+')
        self.lexer.add('STRING', r'".+"')
        self.lexer.add('CHAR', r'\'.\'')

        self.lexer.ignore(r'\s+')
        self.lexer.ignore(r'\n')
        
    def buildLexer(self):
        self._add_tokens()
        return self.lexer.build()