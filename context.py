from data_type import *

class ExecutionContext:
    ''' a context for the cpu to keep track of where it is executing in some program memory

    for example, you would load program code into a context object like this
    and give it to the cpu to execute code from that memory
    also can tell the cpu who is running this program
    that way access can be had to the player's own local ram
    '''

    def __init__(self, memory, player, game, pointer=0):
        # memory is the memory interface providing access to the program
        self.memory = memory

        # the player executing this program
        self.player = player

        # the game instance running this program
        self.game = game

        # pointer is where the cpu is currently looking
        self.jump(pointer)

        # this will tell whether the program has halted or not
        # when a program is finished and wants to exit, it will use the halt operation
        # which will then set this to True
        self.halted = False
        
        # this is the data stack
        self.stack = list()

        # and this is the call stack
        self.call_stack = list()

    def halt(self):
        ''' set the execution to halt '''
        self.halted = True

    def jump(self, address):
        ''' set the pointer, wrapping it around if needed '''
        self.pointer = address % self.memory.length

    def fetch(self, data_type):
        ''' fetch a value from program memory '''
        value, post_address = self.memory.read(self, self.pointer, data_type)
        self.jump(post_address)
        return value

    def fetch_byte(self):
        ''' fetch a byte from program memory '''
        return self.fetch(ByteInterface())

    def fetch_word(self):
        ''' fetch a word from program memory '''
        return self.fetch(WordInterface())

    def fetch_string(self):
        ''' fetch a string from program memory '''
        return self.fetch(StringInterface())

    def fetch_instruction(self):
        ''' fetch a instruction from program memory '''
        return self.fetch(InstructionInterface())
