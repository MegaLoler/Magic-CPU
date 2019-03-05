#!/usr/bin/env python3

# this is the corresponding assembly language for the bytecode
# you can run this file directly in order to assemble a program
# make sure you have the tatsu module installed

# usage: python assembler.py input.asm output.bin

from memory_interface_spec import *
from preprocessor import preprocess
import operation
import data_type
import sys
import tatsu
import tatsu.walkers
import os

"""
    Constants
"""

BYTE_SIZE = 256
WORD_SIZE = 65536

# open and compile the assemebly language grammar for use
cd = os.path.dirname(__file__)
grammar_filename = f'{cd}/grammar.ebnf'
with open(grammar_filename, 'r') as f:
    grammar = f.read()
    parser = tatsu.compile(grammar, asmodel=True)

def parse(code):
    ''' parse code into an ast '''
    return parser.parse(code)

class LabelPlaceholder:
    ''' an object marking the place of a label definition '''
    def __init__(self, name):
        self.name = name

class InstructionPlaceholder:
    ''' an object marking an instruction to be compiled '''
    def __init__(self, opcode_bytes, arguments):
        self.opcode_bytes = opcode_bytes
        self.arguments = arguments

    @property
    def length(self):
        ''' get the amount of bytes that this instruction consumes '''

        class LilWalker(tatsu.walkers.NodeWalker):
            def walk_Byte(self, node):
                return 1

            def walk_Label(self, node):
                return 2

            def walk_Word(self, node):
                return 2

            def walk_String(self, node):
                return len(node.string) + 1

            def walk_Immediate(self, node):
                return self.walk(node.value)

            def walk_Direct(self, node):
                return 2

            def walk_Indirect(self, node):
                return 2

        lil_walker = LilWalker()
        return len(self.opcode_bytes) + sum(map(lil_walker.walk, self.arguments))

class walker(tatsu.walkers.NodeWalker):
    # temporarily replacing this function with the old code so it works for now Dx
    # i'll clean it up like you had it soon enough!
    def lookup_opcode(self, mnemonic, arguments):
        ''' lookup an opcode that corresponds to this mnemonic and these arguments '''

        # this function is a disaster lol
        # some more testing oughtta be done......
        # loop through each opspec to find the match
        class LilWalker(tatsu.walkers.NodeWalker):
            ''' idek care anymore this function has to go '''

            def walk_Byte(self, node):
                return data_type.byte_type

            def walk_Label(self, node):
                return data_type.word_type

            def walk_Word(self, node):
                return data_type.word_type
            
            def walk_String(self, node):
                return data_type.string_type

        lil_walker = LilWalker()

        for opcode in range(len(operation.opspecs)):
            opspec = operation.opspecs[opcode]
            op = operation.opcodes[opcode]

            # make sure the mnemonic matches first, silly
            if op.mnemonic.lower() == mnemonic.lower():

                # and make sure arity matches, too
                if len(opspec) == len(arguments):

                    # loop through each argument
                    # and make sure it matches
                    match = True
                    for i in range(len(opspec)):
                        spec = opspec[i]
                        arg = arguments[i]

                        if arg.__class__.__name__ == 'Immediate':
                            if type(spec) != data_type.ImmediateInterface:
                                match = False
                                break

                            if lil_walker.walk(arg.value).__class__ != spec.data_type.__class__:
                                match = False
                                break

                        else:
                            if arg.__class__.__name__ == 'Direct':
                                if type(spec) != data_type.DirectInterface:
                                    match = False
                                    break

                            elif arg.__class__.__name__ == 'Indirect':
                                if type(spec) != data_type.IndirectInterface:
                                    match = False
                                    break

                            if self.walk(arg.type).__class__ != spec.data_type.__class__:
                                match = False
                                break

                            if self.walk(arg.interface).__class__ != spec.memory_spec.__class__:
                                match = False
                                break

                    if match: return opcode

        # raise a somewhat helpful exception
        args = ', '.join(map(str, arguments))
        raise Exception(f'Failed to find opcode for {mnemonic} with {args}')

    ''' walks the ast generating bytecode '''
    def walk_object(self, node):
        ''' fallback '''
        print(f'[DEBUG] ignoring node {node}')

    def walk_Code(self, node):
        ''' top level ast node '''

        # no labels have been defined yet
        self.labels = {}

        # do an initial walk
        objects = list(map(lambda x: self.walk(x.object), node.objects))

        # filter out empty values
        objects = list(filter(lambda x: x, objects))

        # now skim through and define labels
        # keep track of how many bytes each object will consume
        # so we know what address a label marks when we see one
        address = 0

        for o in objects:

            # if we see a label placeholder
            if isinstance(o, LabelPlaceholder):

                # add that address to the list of known labels!
                self.labels[o.name] = address

            else:
                # otherwise, just count upwards how much bytes are consumed
                address += o.length

        # now filter out the label placeholders
        objects = list(filter(lambda x: not isinstance(x, LabelPlaceholder), objects))

        # now go through it another time and compile the objects to bytes!
        objects = list(map(self.walk, objects))

        # and finally concatenate it all and return
        bytecode = bytes()

        for o in objects:
            bytecode += o

        return bytecode

    def walk_Comment(self, node):
        ''' a comment was read, ignore it '''
        return bytes()

    def walk_VariableDefinition(self, node):
        ''' define this label '''
        self.labels[node.label.string] = self.walk(node.value)[0]
        return bytes()

    def walk_LabelDefinition(self, node):
        ''' put a label placeholder here '''
        return LabelPlaceholder(node.label.string)

    def walk_Instruction(self, node):
        ''' an instruction was read '''

        # get rid of commas n stuff
        arguments = list(filter(lambda x: not isinstance(x, str), node.arguments))

        # first match the argument types with the opspec to get the opcode
        opcode = self.lookup_opcode(node.mnemonic, arguments)

        # compile that opcode into bytes
        opcode_bytes = data_type.OpcodeInterface().compile(opcode)

        # emit an instruction placeholder
        return InstructionPlaceholder(opcode_bytes, arguments)

    def walk_InstructionPlaceholder(self, node):
        ''' resolve the instruction after all labels have been resolved '''

        # then resolve the orguments
        arguments = list(map(self.walk, node.arguments))
        bytecode = node.opcode_bytes

        for a in arguments:
            bytecode += a

        return bytecode

    def walk_Immediate(self, node):
        ''' read an immediate argument '''
        value, data_type = self.walk(node.value)
        return data_type.compile(value)

    def walk_Direct(self, node):
        ''' read an direct argument '''
        # this is an ugly hack
        if node.address.__class__.__name__ == 'Numeral':
            address = self.walk(node.address)
        else:
            address, dt = self.walk(node.address)
        return data_type.word_type.compile(address)

    def walk_Indirect(self, node):
        ''' read an direct argument '''
        # this is an ugly hack
        if node.address.__class__.__name__ == 'Numeral':
            address = self.walk(node.address)
        else:
            address, dt = self.walk(node.address)
        return data_type.word_type.compile(address)

    def walk_Program(self, node):
        return program_memory_spec

    def walk_Player(self, node):
        return player_ram_spec

    def walk_Omni(self, node):
        return omni_ram_spec

    def walk_Label(self, node):
        ''' lookup a label address! '''
        if node.string in self.labels:
            return self.labels[node.string], data_type.word_type
        else:
            raise Exception(f'Unknown label "{node.string}"')

    def walk_Type(self, node):
        return self.walk(node.type)

    def walk_StringType(self, node):
        return data_type.string_type

    def walk_ByteType(self, node):
        return data_type.byte_type

    def walk_WordType(self, node):
        return data_type.word_type

    def walk_String(self, node):
        ''' read a string value '''
        return node.string, data_type.string_type

    def walk_Byte(self, node):
        ''' read a byte value '''
        number = self.walk(node.numeral)
        if number >= BYTE_SIZE: raise Exception(f'The BYTE value {number} is out of range')
        return number, data_type.byte_type

    def walk_Word(self, node):
        ''' read a word value '''
        number = self.walk(node.numeral)
        if number >= WORD_SIZE: raise Exception(f'The WORD value {number} is out of range')
        return number, data_type.word_type

    def walk_Numeral(self, node):
        ''' parse a number '''
        base_test = {'b': 2, 'o': 8, 'h': 16}
        base = base_test[node.base] if node.base in base_test else 10
        return int(node.digits, base)

def assemble(code):
    ''' assemble code as a self contained program written in the assembly language

    return the assembled bytecode
    '''

    # first parse it into an abstract syntax tree
    ast = parse(code)

    # walk the parsed ast generating bytecode
    bytecode = walker().walk(ast)

    # return the bytecode
    return bytecode

if __name__ == '__main__':

    if len(sys.argv) == 3:
        
        # get the source filename and the target binary filenames
        in_filename = sys.argv[1]
        out_filename = sys.argv[2]

        # read in all the source code
        with open(in_filename, 'r') as f:
            print(f'Reading "{in_filename}"...')
            code = f.read()

        # run the preprocessor
        # the preprocessor as is should never be used in game, because it accesses the filesystem
        print('Preprocessing...')
        code = preprocess(in_filename, code)

        # assemble the binary
        print('Assembling...')
        bytecode = assemble(code)

        # write out the binary file
        with open(out_filename, 'wb') as f:
            print(f'Writing assembled program to "{out_filename}"...')
            f.write(bytecode)

        print('All done')

    else: print(f'Usage: python {sys.argv[0]} code.asm output.bin')
