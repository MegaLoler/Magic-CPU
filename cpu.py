import time
from operation import ops

class CPU:
    ''' calling it CPU for now, i know it's supposed to actually be different from a real CPU though '''
    def __init__(self, game):
        # provide the game instance to the cpu in order for it to access the game's omnipresent ram
        self.game = game

    def step(self, context):
        ''' execute the next instruction

        call this function to carry out one operation, to step through the program
        call it repeatedly to run the program continuously
        give it an execution context with the memory containing the program to run
        '''
        # the first thing is to read in an instruction from the bytestream
        # TODO
        # the second thing to do is to execute that instruction
        return instruction.execute(context)

    def run(self, context):
        ''' or call this function and have the cpu run the program until it halts '''
        # continuously step through the program until halted
        while not context.halted:
            self.step(context)
        # and then return the temporary register as the programs "return value"
        return context.register
