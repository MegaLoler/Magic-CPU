from enum import Enum

#prob gonna remove these

class AddressingMode(Enum):
    ''' represents the different kinds of addressing modes
    
    addressing mode is whether the argument is any of the following:
    - immediate: the argument value is embeded directly in the bytestream immediately following the opcode
    - direct: the argument value is located in memory at the address immediately following the opcode
    - indirect: the argumennt value is located in memory at the address specified in memory located at the address immediately following the opcode
    '''
    IMMEDIATE = 1
    DIRECT = 2
    INDIRECT = 3

class DataType(Enum):
    ''' represents the different data types
    
    data type is what kind of data it is, obviously, haha, and is any of the following:
    - byte (8 bit value)
    - word (16 bit value)
    - string (a series of ascii encoded characters terminated with a null byte (= 0))
    '''
    BYTE = 1
    WORD = 2
    STRING = 3

class MemoryTarget(Enum):
    ''' represents the different possible memories to be accessed

    - program memory, refers to the memory the program is running from
    - player memory, refers to each player's individual ram
    - omni memory, refers to the omnipresent ram in a game instance
    '''
    PROGRAM = 1
    PLAYER = 2
    OMNI = 3

class Argument:
    ''' represents an argument to an instruction

    an instruction argument designates a value to be resolved at the time of executing that instruction
    '''
    def __init__(self, value, addressing_mode=AddressingMode.IMMEDIATE, data_type, memory):
        self.value = value
        self.addressing_mode = addressing_mode
        self.data_type = data_type
        self.memory = memory

    def read(self, context):
        ''' read the value that htis argument represents at runtime in an execution context '''
        # TODO

    def write(self, context, value):
        ''' write a value to a location represented by this argument at runtime '''
        # TODO
