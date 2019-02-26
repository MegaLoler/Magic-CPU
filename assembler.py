#!/usr/bin/env python3

# this is the corresponding assembly language for the bytecode
# you can run this file directly in order to assemble a program

import tatsu
import tatsu.walkers

# open and compile the assemebly language grammar for use
with open('grammar.ebnf', 'r') as f:
    grammar = f.read()
    parser = tatsu.compile(grammar, asmodel=True)

def parse(code):
    ''' parse code into an ast '''
    return parser.parse(code)

class walker(tatsu.walkers.NodeWalker):
    ''' walks the ast generating bytecode '''

def assemble(code):
    ''' assemble code as a self contained program written in the assembly language

    return the assembled bytecode
    '''
    # first parse it into an abstract syntax tree
    ast = parse(code)
    # walk the parsed ast generating bytecode
    bytecode = walker.walk(ast)
    # return the bytecode
    return bytecode

if __name__ == '__main__':
    if len(sys.argv) == 3:
        in_filename = sys.argv[1]
        out_filename = sys.argv[2]
        with open(in_filename, 'r') as f:
            print(f'Reading {in_filename}...')
            code = f.read()
        print('Assembling...')
        bytecode = assemble(code)
        with open(out_filename, 'wb') as f:
            print('Writing assembled program to {out_filename}...')
            f.write(bytecode)
        print('All done')
        
    else: print(f'Usage: python {sys.argv[0]} code.asm output.bin')
