from argument import Literal
from memory_interface_spec import *
from data_type import *
import util
import time

# an array of opspecs, arranged such that index = opcode
# an opspec is a list of parameters, indicating how many arguments, and the nature of them
# a parameter is just a data type interface, for reading the argument from a stream
opspecs = list()

# an array of operations, such that index = opcode corresponding to the operation
opcodes = list()

# a global dictionary for looking up operations by mnemonic
ops = dict()

def dir_ops():
    ''' print a listing of opcodes and their parameters '''
    for opcode in range(len(opcodes)):
        operation = opcodes[opcode]
        opspec = opspecs[opcode]
        opcode_string = format(opcode, '02x')
        def par_spec(parameter):
            target = parameter.__class__.__qualname__
            data_type = parameter.data_type.__class__.__qualname__
            if isinstance(parameter, ImmediateInterface):
                return f'{data_type} : {target}'
            else:
                interface = parameter.memory_spec.__class__.__qualname__
                return f'{data_type} : {target} : {interface}'
        parameter_spec_string = list(map(par_spec, opspec))
        print(f'0x{opcode_string} {operation.mnemonic} {parameter_spec_string}')

def register_opcode(operation, opspec):
    ''' allocate a new opcode and add an operation to opcodes and the opspec to opspecs '''
    # add it to opspecs and opcodes
    # it's assumed that this function is the only time these lists are appended
    # so the opcode value should stay the syncronized
    opcodes.append(operation)
    opspecs.append(opspec)

def generate_opspecs(operation, parameter_type_spec):
    ''' generate opspecs for different possible argument configurations '''
    # create a list of all possible opspecs
    # type x addressing mode x memory interface
    # first list off possible targets
    # my brain is dead but theres a much better way to generate this stuff
    targets = (
            ImmediateInterface,
            lambda t: DirectInterface(program_memory_spec, t),
            lambda t: DirectInterface(player_ram_spec, t),
            lambda t: DirectInterface(omni_ram_spec, t),
            lambda t: IndirectInterface(program_memory_spec, t),
            lambda t: IndirectInterface(player_ram_spec, t),
            lambda t: IndirectInterface(omni_ram_spec, t),
            )
    # now get a list of possible target combinations matching the arity...
    target_combinations = util.combinations((targets,) * len(parameter_type_spec))
    # now get a list of possible type combinations...
    type_combinations = util.combinations(parameter_type_spec)
    # now pair target combos with type combos...
    pairs = util.combinations((type_combinations, target_combinations))
    # now create an opspec for each pair
    if len(pairs):
        for pair in pairs:
            opspec = list()
            type_spec, target_spec = pair
            for i in range(len(type_spec)):
                data_type = type_spec[i]()
                target = target_spec[i]
                opspec.append(target(data_type))
            # register the opspec
            register_opcode(operation, opspec)
    else:
        # this is for the case of an arity of 0
        register_opcode(operation, list())

class Operation:
    ''' represents an operation that the cpu can carry out, its assemebly mnemonic, and its function '''
    def __init__(self, mnemonic, handler):
        # mnemonic is the name used in assembly language instructions to refer to this operation
        self.mnemonic = mnemonic
        # handler is the function used to carry out this operation
        self.handler = handler

def op(*parameter_type_spec):
    ''' return a decorator for defining operations
    
    to define an operation, decorate it with @op(...)
    whose arguments are a list of accepted data type interfaces per each argument
    '''
    def decorator(handler):
        ''' decorator for defining operations '''
        # use the decorated functions name as the op mnemonic
        # and the function itself as the operation handler
        operation = Operation(handler.__name__, handler)
        # register it by mnemonic in the global op dict
        ops[operation.mnemonic] = operation
        # finally generate opspecs for different possible parameters
        generate_opspecs(operation, parameter_type_spec)
        return operation
    return decorator

@op()
def nop(context):
    ''' this op does nothing '''
    pass

@op((ByteInterface, WordInterface,),)
def wait(context, duration):
    ''' wait some amount of seconds before continuing program execution, useful for debugging '''
    time.sleep(duration.value)

@op((ByteInterface, WordInterface, StringInterface,),)
def echo(context, value):
    ''' print some value to console, also useful for debugging '''
    print(value.value)

@op((WordInterface,),)
def jmp(context, address):
    ''' jump unconditionally to some location in program memory and continue executing from there '''
    context.jump(address.value)

@op((ByteInterface,),)
def halt(context, value):
    ''' halt program execution, signalling that the program is finished

    the argument will be returned when the program exits
    '''
    context.halt(value.value)

# for ease of testing, run this file to get a printout of op codes
if __name__ == '__main__': dir_ops()
