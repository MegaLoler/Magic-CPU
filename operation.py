from argument import Literal
import time

# an array of opspecs, arranged such that index = opcode
# an opspec is a list of parameters, indicating how many arguments, and the nature of them
# a parameter is just a data type interface, for reading the argument from a stream
opspecs = list()

# an array of operations, such that index = opcode corresponding to the operation
opcodes = list()

# a global dictionary for looking up operations by mnemonic
ops = dict()

class Operation:
    ''' represents an operation that the cpu can carry out, its assemebly mnemonic, and its function '''
    def __init__(self, mnemonic, handler):
        # mnemonic is the name used in assembly language instructions to refer to this operation
        self.mnemonic = mnemonic
        # handler is the function used to carry out this operation
        self.handler = handler

def op():
    ''' return a decorator for defining operations '''
    def decorator(handler):
        ''' decorator for defining operations '''
        # use the decorated functions name as the op mnemonic
        # and the function itself as the operation handler
        op = Operation(handler.__name__, handler)
        # register it by mnemonic in the global op dict
        ops[op.mnemonic] = op
        # finally generate opspecs for different possible parameters

        return op
    return decorator

@op()
def nop(context):
    ''' this op does nothing '''
    pass

@op()
def wait(context, duration=Literal(1)):
    ''' wait some amount of seconds before continuing program execution, useful for debugging '''
    time.sleep(duration.value)

@op()
def print(context, value):
    ''' print some value to console, also useful for debugging '''
    print(value.value)
