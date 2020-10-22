#!/usr/bin/env python3

''' bfc
This is code generator for bfc. 
'''

class BFCodeGenerator:
    ''' This is the core of bfc that will actually compile the command into brainfsck.
    It holds the state (and positions in memory) of variables and cell positions.
    
    Most of the brainfsck algorithms are really simple, for a list of more complex
    brainfsck algorithms see https://esolangs.org/wiki/Brainfuck_algorithms
    '''
    def __init__(self):
        ''' Initial state of the program
        code: holds brainfsck commands
        cell_index: the current memory cell index needed by the compiler to ensure 
                    variables are pointing to the correct place in memory.
        variables: a list of the variables from the source files and their memory 
                   cell positions.
        '''
        self.code = ""
        self.cell_index = 0;
        self.variables = {}
        
    def assign(self, var, value):
        if var in self.variables:
            self.zero(var) # zero the variable before we assign a new number
        else:
            # create a new variable
            self.variables[var] = len(self.variables)
        self.increment(var, amount=value)        

    def increment(self, var, amount=1):
        self.moveTo(var)
        for i in range(0,amount):
            self.code += '+'

    def decrement(self, var, amount=1):
        self.moveTo(var)
        for i in range(0,amount):
            self.code += '-'
        
    def moveTo(self, var):
        ''' "moves to" the memory cell of a variable '''
        cell = self.variables[var]
        index = self.cell_index
        if cell > index:
            for i in range(cell-index):
                self.code += '>'
                self.cell_index += 1
        elif cell < index:
            for i in range(index-cell):
                self.code += '<'
                self.cell_index -= 1
                
    def zero(self, var):
        self.moveTo(var)
        self.code += '[-]'
        
    def printascii(self, var):
        self.moveTo(var)
        self.code += '.'
    
    def printchar(self, char,  temp):
        temp = 'temp1'
        self.zero(temp)
        self.increment(temp, amount=char)
        self.code += '.'
        
    def printstr(self, string, temp):
        ''' print a string
        will change the values of the cell temp'''
        # first we zero the cell
        self.zero(temp)
        current = 0
        for c in string:
            new = ord(c) - current
            if new > 0:
                self.increment(temp, new)
            elif new < 0:
                self.decrement(temp, abs(new))
            current = current + new
            
            self.printascii(temp)
        
    def printnum(self, var, temp):
        ''' This algorithmm will take the cell value and print the ascii values of the digits '''
        self.moveTo(var)
        self.code += '''[>>+>+<<<-]>>>[<<<+>>>-]<<+>[<->[>++++++++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]++++++++[<++++++>-]>[<<+>>-]>[<<+>>-]<<]>]<[->>++++++++[<++++++>-]]<[.[-]<]<'''
        #self.code += '''>>++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++<]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]<'''    
                
    def readascii(self, var):
        self.moveTo(var)
        self.code += ','
        
    def add(self, var, var2):
        self.loopOpen(var)
        self.decrement(var)
        self.increment(var2)
        self.loopEnd(var)        

    def copy(self, var, others):
        self.loopOpen(var)
        self.decrement(var)
        for c in others:
            self.increment(c)
        self.loopEnd(var)
        
    def loopOpen(self, var):
        self.moveTo(var)
        self.code += '['
        
    def loopEnd(self, var):
        self.moveTo(var)
        self.code += ']'
                
    def ifOpen(self, var, temp):
        self.zero(temp)
        self.loopOpen(var)
        
    def ifEnd(self, var, temp):
        self.loopEnd(temp)
        self.moveTo(var)
        
    def ifElseOpen(self, var, temp0, temp1):
        self.zero(temp0)
        self.increment(temp0)
        self.zero(temp1)
        self.loopOpen(var)
    
    def ifElse(self, var, temp0, temp1):
        self.decrement(temp0)
        self.copy(var, [temp1])
        self.loopEnd(var)
        self.copy(temp1, [var])
        self.loopOpen(temp0)   
    
    def ifElseEnd(self, var, temp0, temp1):
        self.decrement(temp0)
        self.loopEnd(temp0)
        
        
        