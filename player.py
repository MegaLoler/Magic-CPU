from context import ExecutionContext

# this is just a dummy player class
# to show players having their own ram
class Player:
    def __init__(self):
        self.ram = bytes(2**10) # 1kb of ram, of course it can be however much you like!

    # make this player run a program using some cpu
    def run_program(self, program, cpu):
        # create the context for execution
        # the program memory is the provided program data
        # and the player is this player!
        context = ExecutionContext(program, self)
        # and tell the cpu to run indefinitely!
        return cpu.run(context)
