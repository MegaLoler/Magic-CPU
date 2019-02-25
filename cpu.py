import time
from operation import ops

# calling it CPU for now, i know it's supposed to actually be different from a real CPU though
class CPU:
    def __init__(self, game):
        # provide the game instance to the cpu in order for it to access the game's omnipresent ram
        self.game = game

    # call this function to execute one operation, to step through the program
    # call it repeatedly to run the program continuously
    # give it an execution context with the memory containing the program to run
    def step(self, context):
        # the first thing to do, is to fetch the op code
        opcode = context.fetch()
        # then lookup the function to handle that operation!
        handler = ops[opcode]
        # and call it if it exists
        if handler: handler(context)

    # or call this function and have the cpu run the program until it halts
    def run(self, context):
        # continuously step through the program until halted
        while not context.halted:
            self.step(context)
        # and then return the temporary register as the programs "return value"
        return context.register
