class Instruction:
    ''' a class representing an instruction

    an instruction is a piece of code that designates an operation for the cpu to carry out
    '''
    def __init__(self, operation, arguments):
        self.operation = operation
        self.arguments = arguments

    def execute(self, context):
        ''' execute this instruction in the execution context provided '''
        self.operation.handler(context, *self.arguments)
