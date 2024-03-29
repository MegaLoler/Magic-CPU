class CPU:
    ''' calling it CPU for now, i know it's supposed to actually be different from a real CPU though '''
    
    def step(self, context):
        ''' execute the next instruction

        call this function to carry out one operation, to step through the program
        call it repeatedly to run the program continuously
        give it an execution context with the memory containing the program to run
        '''

        # the first thing is to read in an instruction from the bytestream
        instruction = context.fetch_instruction()

        # the second thing to do is to execute that instruction
        return instruction.execute(context)

    def run(self, context, arguments=list()):
        ''' or call this function and have the cpu run the program until it halts '''

        # load the program arguments into the data stack
        context.stack = arguments

        # continuously step through the program until halted
        while not context.halted:
            self.step(context)

        # return the data stack as the final return value(s)
        return context.stack
