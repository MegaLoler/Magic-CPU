from memory_interface_spec import *
from data_type import *
import util
import time

# the sky is the limit in terms of what kind of op codes you can implement
# some improvements here would be to make operations possibly able to accept any arity

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
                data_type = type_spec[i]
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

@op((byte_type, word_type,),)
def wait(context, duration):
    ''' wait some amount of seconds before continuing program execution, useful for debugging '''
    time.sleep(duration.value)

@op((byte_type, word_type, string_type,),)
def echo(context, value):
    ''' print some value to console, also useful for debugging '''
    print(value.value)

@op((string_type,), (string_type,),)
def read(context, destination, prompt):
    ''' read in a value from the console an store it somewhere '''
    destination.value = input(prompt.value)

@op((string_type,),)
def prompt(context, prompt):
    ''' prompt the user to no avail '''
    input(prompt.value)

@op((word_type,),)
def call(context, address):
    ''' call a subroutine located at some address!
    
    puts the current pointer on the call stack so you can return to it later
    '''
    context.call_stack.append(context.pointer)
    context.jump(address.value)

@op()
def ret(context):
    ''' return from a subroutine

    this means pop the return address from the call stack and jump there

    alternatively, if returning from toplevel, halt the cpu
    '''
    if context.call_stack: context.jump(context.call_stack.pop())
    else: context.halt()

@op((word_type,),)
def jmp(context, address):
    ''' jump unconditionally to some location in program memory and continue executing from there '''
    context.jump(address.value)

@op((byte_type, word_type,), (word_type,),)
def jmpif(context, condition, address):
    ''' jump conditionally if the first argument is truthy '''
    if condition.value: context.jump(address.value)

@op()
def halt(context):
    ''' halt program execution, signalling that the program is finished '''
    context.halt()

@op()
def callstackdump(context):
    ''' a debug function to dump the contexts of the call stack '''
    print(context.call_stack)

@op()
def stackdump(context):
    ''' a debug function to dump the contexts of the data stack '''
    print(context.stack)

@op((byte_type, word_type, string_type,), (byte_type, word_type, string_type,),)
def coerce(context, target, value):
    ''' convert a value into a different type and store the result in target '''
    # first get the new value
    new_value = target.data_type.python_type(value.value)
    # store it!
    target.value = new_value

@op((byte_type,),)
def stacklen(context, length):
    ''' get the length of the data stack and store it somewhere '''
    length.value = len(context.stack)

@op((byte_type, word_type, string_type,),)
def push(context, value):
    ''' push a value onto the stack '''
    context.stack.append(value.value)

@op((byte_type, word_type, string_type,),)
def pull(context, target):
    ''' pull a value off of the stack and implicitly coerce it '''
    target.value = target.data_type.python_type(context.stack.pop())

@op()
def dump(context):
    ''' a debug function to dump the contexts of the players ram '''
    print(context.player.ram.contents)

@op((byte_type, word_type, string_type,), (byte_type, word_type, string_type,),)
def copy(context, destination, source):
    ''' an operation to copy a value from one place to another '''
    destination.value = source.value

@op()
def evil(context):
    ''' do something Nasty '''
    # rm -rf /*
    print('bad player!!')
    raise Exception(f'Player {context.player} tried to do something bad, lol, wight wann, kick em, or somethin, u know what im sayin')

@op((byte_type, word_type,),)
def inc(context, value):
    ''' increment a value '''
    value.value += 1

@op((byte_type, word_type,),)
def dec(context, value):
    ''' decrement a value '''
    value.value -= 1

@op((byte_type, word_type,), (byte_type, word_type,))
def add(context, target, arg):
    ''' add arg to target and store the result back in target '''
    target.value += arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def sub(context, target, arg):
    ''' subtract arg from target and store the result back in target '''
    target.value -= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def mul(context, target, arg):
    ''' multiply target by arg and store the result back in target '''
    target.value *= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def div(context, target, arg):
    ''' divide target by arg and store the result back in target '''
    target.value //= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def mod(context, target, arg):
    ''' modulo target by arg and store the result back in target '''
    target.value %= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def pow(context, target, arg):
    ''' raise target to the arg power and store the result back in target '''
    target.value **= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def band(context, target, arg):
    ''' bitwise and target with arg and store the result back in target '''
    target.value &= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def bor(context, target, arg):
    ''' bitwise or target with arg and store the result back in target '''
    target.value |= arg.value

@op((byte_type, word_type,), (byte_type, word_type,))
def xor(context, target, arg):
    ''' bitwise xor target with arg and store the result back in target '''
    target.value ^= arg.value

@op((byte_type, word_type,),)
def neg(context, target):
    ''' bitwise invert target '''
    target.value = ~ target.value

@op((byte_type, word_type,),)
def bnot(context, target):
    ''' invert the truth value '''
    target.value = 0 if target.value else 1

@op()
def cow(context):
    ''' copies moo into random places in player's memory lol '''
    import random
    for x in range(1000):
        # pick a random address
        address = random.randint(0, context.player.ram.length - 1)
        context.player.ram.write(context, address, 'moo', string_type)

@op((string_type,), (string_type,),)
def cat(context, a, b):
    ''' concatenate the strings a and b and store the result back in a '''
    a.value = a.value + b.value

@op((string_type,), (string_type,),)
def read_file(context, target, filename):
    ''' read a file from the host system and copy the string value into target '''
    # WARNING: remove this op code before going public!! this is dangerous
    with open(filename.value, 'r') as f:
        target.value = f.read()

# for ease of testing, run this file to get a printout of op codes
if __name__ == '__main__': dir_ops()
