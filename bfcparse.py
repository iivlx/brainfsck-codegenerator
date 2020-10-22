#!/usr/bin/env python3

''' bfc
This is the parser for bfc. The source file is tokenized and passed into the
parser, which will create a parse tree that can be executed to produce
brainfsck code.
'''

from rply import ParserGenerator
from rply.token import BaseBox
from numpy.core.fromnumeric import var

class Line(BaseBox):
    def __init__(self, value):
        self.value = value
        
    def eval(self):
        return self.value.eval()

class Number(BaseBox):
    def __init__(self, value):
        self.value = value
        
    def eval(self):
        return self.value
    
class Variable(BaseBox):
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        return self.value
    
class String(BaseBox):
    def __init__(self, value):
        self.value = value[1:-1]
    
    def eval(self):
        return self.value
    
class Increment(BaseBox):
    def __init__(self, state, left, right):
        self.state = state
        self.left = left
        self.right = right
    def eval(self):
        # add the right to the left
        l = self.left.eval()
        r = self.right.eval()
        self.state.increment(l, amount=r)
#         print('Incrementing %s by %d' %(l, r)) # sponge

class Loop(BaseBox):
    def __init__(self, state, var):
        self.state = state
        self.var = var
    def eval(self):
        self.state.loopOpen(self.var.eval())
        
class LoopEnd(BaseBox):
    def __init__(self, state, var):
        self.state = state
        self.var = var
    def eval(self):
        self.state.loopEnd(self.var.eval())

class IfOpen(BaseBox):
    def __init__(self, state, var, temp):
        self.state = state
        self.var = var
        self.temp = temp
    def eval(self):
        self.state.ifOpen(self.var.eval(), self.temp.eval())
        
class IfEnd(BaseBox):
    def __init__(self, state, var, temp):
        self.state = state
        self.var = var
        self.temp = temp
    def eval(self):
        self.state.ifEnd(self.var.eval(), self.temp.eval())
    
class IfElseOpen(BaseBox):
    def __init__(self, state, var, temp0, temp1):
        self.state = state
        self.var = var
        self.temp0 = temp0
        self.temp1 = temp1
    def eval(self):
        self.state.ifElseOpen(self.var.eval(), self.temp0.eval(), self.temp1.eval())
        
class IfElse(BaseBox):
    def __init__(self, state, var, temp0, temp1):
        self.state = state
        self.var = var
        self.temp0 = temp0
        self.temp1 = temp1
    def eval(self):
        self.state.ifElse(self.var.eval(), self.temp0.eval(), self.temp1.eval())

class IfElseEnd(BaseBox):
    def __init__(self, state, var, temp0, temp1):
        self.state = state
        self.var = var
        self.temp0 = temp0
        self.temp1 = temp1
    def eval(self):
        self.state.ifElseEnd(self.var.eval(), self.temp0.eval(), self.temp1.eval())
            
class Decrement(BaseBox):
    def __init__(self, state, left, right):
        self.state = state
        self.left = left
        self.right = right
    def eval(self):
        # add the right to the left
        l = self.left.eval()
        r = self.right.eval()
        self.state.decrement(l, amount=r)
        #print('Decrementing %s by %d' %(l, r))

class Assignment(BaseBox):
    def __init__(self, state, left, right):
        self.state = state
        self.left = left
        self.right = right
    def eval(self):
        l = self.left.eval()
        r = self.right.eval()
        self.state.assign(l, r)
        # sponge
#         self.state.variables[l] = len(self.state.variables)
#         self.state.zero(l)
#         self.state.increment(l, amount=r)        
#         print('Assigning %d to %s' % (r, l)) # assign right to left

class Print(BaseBox):
    def __init__(self, value):
        self.value = value
    def eval(self):
        print(self.value.eval())

class PrintI(BaseBox):
    def __init__(self, state, value):
        self.state = state
        self.value = value
    def eval(self):
        self.state.printascii(self.value)

class PrintNum(BaseBox):
    def __init__(self, state, value, temp):
        self.state = state
        self.value = value
        self.temp = temp
    def eval(self):
        self.state.printnum(self.value.eval(), self.temp.eval())

class PrintC(BaseBox):
    def __init__(self, state, value, temp):
        self.state = state
        self.value = value
        self.temp = temp
    def eval(self):
        self.state.printchar(self.value.eval(), self.temp.eval())

class PrintS(BaseBox):
    def __init__(self, state, value, temp):
        self.state = state
        self.value = value
        self.temp = temp
    def eval(self):
        self.state.printstr(self.value.eval(), self.temp.eval())
        
class AddVars(BaseBox):
    def __init__(self, state, left, right):
        self.state = state
        self.left = left
        self.right = right
    def eval(self):
        self.state.add(self.left.eval(), self.right.eval())

class Copy(BaseBox):
    def __init__(self, state, left, others):
        self.state = state
        self.left = left
        self.others = others
    def eval(self):
        list = []
        for o in self.others:
            list.append(o.eval())
        self.state.copy(self.left.eval(), list)

class Read(BaseBox):
    def __init__(self, state, var):
        self.state = state
        self.var = var
    def eval(self):
        self.state.readascii(self.var.eval())

class Trace(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())
        
class Comment(BaseBox):
    def __init__(self):
        pass
    def eval(self):
        pass
        
class BinaryOperation(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
class Add(BinaryOperation):
    def eval(self):
        return self.left.eval() + self.right.eval()
class Sub(BinaryOperation):
    def eval(self):
        return self.left.eval() - self.right.eval()
class Mul(BinaryOperation):
    def eval(self):
        return self.left.eval() * self.right.eval()
class Div(BinaryOperation):
    def eval(self):
        return self.left.eval() / self.right.eval()

class Parser:
    def __init__(self):
        ''' Initialize valid tokens
        todo: dynamic token list'''
        self.pg = ParserGenerator(['NUMBER',
                                   'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
                                   'EQUALS',
                                   'PLUSEQUALS', 'MINUSEQUALS',
                                   'VAR',
                                   'IF', 'ELSE',
                                   'WHILE',
                                   'END', 'ENDIF',
                                   'SEMICOLON',
                                   'COLON',
                                   'PRINT', 'PRINTNUM',
                                   'ADD',
                                   'COPY',
                                   'IDENTIFIER',
                                   'NOP',
                                   'READASCII',
                                   'STRING', 'CHAR',
                                   'TRACE', 'COMMENT'])
        
    def parse(self):
        ''' Parse each line and token of the program into a tree, using the code generator state.
        todo: there really should be a list of valid syntax...
        '''
        @self.pg.production('program : program line')
        @self.pg.production('program : line')
        def p_program(state, p):
            if len(p) == 1:
                return [*p[0]]
            elif len(p) == 2:
                return [*p[0],*p[1]]

        @self.pg.production('line : IDENTIFIER EQUALS expression SEMICOLON')
        def p_line(state, p):
            return Line(p[:-1])
        
        @self.pg.production('line : loop COLON loopbody END SEMICOLON')
        def p_line_loop(state, p):
            
            loop = p[0]
            loopend = LoopEnd(state, p[0].var)
            
            return [loop, *p[2], loopend]

        @self.pg.production(' line : if COLON ifbody ELSE ifbody ENDIF SEMICOLON')
        def p_line_if_else(state, p):
            if_start = IfElseOpen(state, p[0], Variable('temp0'), Variable('temp1'))
            if_else = IfElse(state, if_start.var, Variable('temp0'), Variable('temp1'))
            if_end = IfElseEnd(state, if_start.var, Variable('temp0'), Variable('temp1'))
            return [if_start, *p[2], if_else, *p[4], if_end]
            #return [Comment()]

        @self.pg.production('line : if COLON ifbody ENDIF SEMICOLON')
        def p_line_if(state, p):
            if_start = IfOpen(state, p[0], Variable('temp0'))
            if_end = IfEnd(state, if_start.var, Variable('temp0'))
            return [if_start, *p[2], if_end]
        
        @self.pg.production('line : COMMENT')
        def p_line_comment(state, p):
            return [Comment()]
        
        @self.pg.production('line : VAR IDENTIFIER SEMICOLON')
        def p_line_var(state, p):
            identifier = p[1].getstr()
            return [Line(Assignment(state, Variable(identifier), Number(0)))]
                
        @self.pg.production('line : VAR IDENTIFIER PLUSEQUALS expression SEMICOLON')
        @self.pg.production('line : VAR IDENTIFIER MINUSEQUALS expression SEMICOLON')
        def p_line_var_op_equals(state, p):
            identifier = p[1].getstr()
            operator = p[2].gettokentype()
            expression = p[3]
            if operator == 'PLUSEQUALS':
                return [Line(Increment(state, Variable(identifier), expression))]
            elif operator == 'MINUSEQUALS':
                return [Line(Decrement(state, Variable(identifier), expression))]
        
        @self.pg.production('line : VAR IDENTIFIER EQUALS expression SEMICOLON')
        def p_line_var_equals(state, p):
            identifier = p[1].getstr()
            expression = p[3]
            return [Line(Assignment(state, Variable(identifier), expression))]
        
        @self.pg.production('line : statement SEMICOLON')
        def p_line_statement(state, p):
            return [Line(p[0])]
        
        @self.pg.production('statement : ADD IDENTIFIER IDENTIFIER')
        def p_add(state, p):
            return AddVars(state, Variable(p[1].getstr()), Variable(p[2].getstr()))
                
        @self.pg.production('statement : COPY IDENTIFIER IDENTIFIER IDENTIFIER')
        def p_copy2(state, p):
            return Copy(state, Variable(p[1].getstr()), (Variable(p[2].getstr()), Variable(p[3].getstr())))
        
        @self.pg.production('statement : COPY IDENTIFIER IDENTIFIER')
        def p_copy(state, p):
            return Copy(state, Variable(p[1].getstr()), (Variable(p[2].getstr()),))

        @self.pg.production('statement : READASCII IDENTIFIER')
        def p_readascii(state, p):
            return Read(state, Variable(p[1].getstr()))

        @self.pg.production('statement : PRINTNUM expression')
        def p_print(state, p):
            return PrintNum(state, p[1], Variable('temp0'))

        @self.pg.production('statement : PRINT expression')
        def p_print(state, p):
            return PrintC(state, p[1], Variable('temp0'))
        
        @self.pg.production('statement : PRINT string')
        def p_print_s(state, p):
            return PrintS(state, p[1], Variable('temp0'))
            
        @self.pg.production('statement : PRINT IDENTIFIER')
        def p_print_v(state, p):
            identifier = p[1].getstr()
            return PrintI(state, identifier)
            
        @self.pg.production('statement : TRACE IDENTIFIER')
        @self.pg.production('statement : TRACE string')
        @self.pg.production('statement : TRACE expression')
        def p_trace(state, p):
            #print( p )
            return Trace(p[1])
            #return Print(p[1])
            
        @self.pg.production('if : IF expression')
        def p_if(state, p):
            return p[1]
        
        @self.pg.production('ifbody : ifbody line')
        @self.pg.production('ifbody : line')
        def p_ifbody(state, p):
            if len(p) == 1:
                return p[0]
            elif len(p) == 2:
                return [*p[0],*p[1]]       

        @self.pg.production('loop : WHILE expression')
        def p__while(state, p):
            return Loop(state, p[1])
        
        @self.pg.production('loopbody : loopbody line')
        @self.pg.production('loopbody : line')
        def p_loopbody(state, p):
            if len(p) == 1:
                return p[0]
            elif len(p) == 2:
                return [*p[0],*p[1]]
        
        @self.pg.production('string : STRING')
        def p_string(state, p):
            return String(p[0].getstr())

        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression MINUS expression')
        @self.pg.production('expression : expression MULTIPLY expression')
        @self.pg.production('expression : expression DIVIDE expression')
        def expression(state, p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'PLUS':
                return Add(left, right)
            if operator.gettokentype() == 'MINUS':
                return Sub(left, right)
            return p    

        @self.pg.production('expression : NUMBER')
        def p_expression_number(state, p):
            return Number(int(p[0].getstr()))
        
        @self.pg.production('expression : IDENTIFIER')
        def p_expression_identifier(state, p):
            return Variable(p[0].getstr())
        
        @self.pg.production('expression : CHAR')
        def p_expression_char(state, p):
            return Number(ord(p[0].getstr()[1]))
    
        @self.pg.error
        def error_handler(state, token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())
    
    def buildParser(self):
        return self.pg.build()