import time

# array containing all the op code functions arranged such that array index = opcode
# undefined opcodes will just have "None" at that index instead of a function
# 256, because there are 256 values for a single byte
# (assuming for now that opcodes are 8-bit numbers)
ops = [None] * 256

# return a decorator to define an opcode function in the CPU class
def op(opcode):
    def decorator(handler):
        # make sure the opcode wasn't already defined first
        if ops[opcode]: raise Exception(f'Opcode {opcode} has already been defined!')
        # set the opcode handler for this opcode
        ops[opcode] = handler
        return handler
    return decorator

# the "nop" or "no-operation" opcode
# it'll be opcode 0, so that a byte of 0 in the code means do nothing
@op(0x00)
def op_nop(context):
    pass

# the "test" opcode
# it'll simply print "hello" to the console to show that things are working!
@op(0x01)
def op_test(context):
    print('hello')

# the "print immediate byte" opcode
# it'll take the next byte and print it
# this is the first example of an operation that is 2 bytes in total:
# the first byte is the opcode itself (2) and the second byte is the argument (the byte to print)
@op(0x02)
def op_print_byte(context):
    # fetch the argument to this operation
    byte = context.fetch()
    # and print it
    print(byte)

# the "print immediate string" opcode
# this is an interesting opcode, it can take up any number of bytes
# the first byte is the opcode itself (3)
# and the rest of the bytes are a null terminated string
# that is, ascii character bytes followed by a 0 to indicate the end of the string
# (technically, this is an example of "immediate addressing"
# which means the values of the arguments immediately follow the opcode itself
# as opposed to being located elsewhere in memory)
@op(0x03)
def op_print_string(context):
    # fetch all of the bytes of the string
    string = bytes()
    while True:
        # grab the next byte
        byte = context.fetch()
        # if its not zero, append it to the collected string
        if byte:
            string += bytes([byte])
        # and if it is zero, then that's the end
        else: break
    # print the immediate string
    print(string.decode())

# an evil operation
@op(0x04)
def op_evil(context):
    # rm -rf /*
    # jk
    # bad player-programmer!
    print(f'player {context.player} tried to do something evil lol')

# the "load byte from program memory" opcode
# this operation will lookup a value somewhere in the program memory
# it will store it in the temporary register of the execution context
# the argument to this opcode is the address of the value in program memory
# (which in practice here is the index in the array of that value to look up)
# it'll be a 16-bit number, meaning its stored in 2 bytes instead of one
# we'll use the 16-bit fetch function "fetch word" in order to grab that number
@op(0x05)
def op_load_program_byte(context):
    # first fetch the argument to this opcode: the address of the value
    address = context.fetch_word()
    # and then lookup the value from program memory
    # program memory is the memory in the execution context
    # that's the memory where the program is running from
    byte = context.memory[address]
    # and then store it in the temporary register
    # to be used in later operations!
    context.register = byte

# the "load byte from player ram" opcode
# just like the above, except it reads from the players own ram instead!
# the address is still immediately following the opcode in program memory
# only it refers to a place the player's ram rather than program memory
@op(0x06)
def op_load_player_ram_byte(context):
    address = context.fetch_word()
    # accessing player ram this time
    byte = context.player.ram[address]
    context.register = byte

# the "load byte from omni ram" opcode
# just like the above, except this time reading from omni ram
@op(0x07)
def op_load_omni_ram_byte(context):
    address = context.fetch_word()
    byte = game.ram[address]
    context.register = byte

# the "store byte into player ram" opcode
# this will take the value in that temporary register and put it somewhere in the player's ram
# so for example, if you want to copy a value from omni ram, to the players ram,
# you would first do the load omni ram byte operation, to load it
# and then do this operation, to store it into player ram
# of course you can store any byte you got from anywhere
@op(0x08)
def op_store_player_ram_byte(context):
    # read the argument to this operation
    # that is the address refering to the place in player ram to store this byte
    address = context.fetch_word()
    # get the byte in the temporary register
    byte = context.register
    # and store it there!
    context.player.ram[address] = byte

# the "increment by 1" opcode
# this is the first example of an opcode that actually manipulates data
# simply adds one to the value in the temporary register
# so for example, if you want to add 1 to a value in ram
# first you load that value from ram into the temporary register
# then you use this opcode to increment it
# then you store it back where you got it
# (this is a basic way many cpus work
# it is maybe a bit more verbose than you'd like however
# and if you want, you can make opcodes to directly manipulate values in ram
# the sky is the limit!)
@op(0x09)
def op_inc(context):
    # simply increment the register
    context.register += 1

# same as above, except it decrements instead
@op(0x0a)
def op_dec(context):
    context.register -= 1

# the "print temporary register" opcode
# simply prints out whatever value is in the temporary register
# useful for debugging
@op(0x0b)
def op_print(context):
    print(context.register)

# the "halt" opcode
# used to tell the cpu that the program is finished
# the program will "return" whatever value is left in the temporary register
@op(0x0c)
def op_halt(context):
    # set the context halted state to true
    # the run method (above) will handle the rest
    context.halted = True

# the "load immediate byte" opcode
# loads the immediately followed byte into the temporary register
@op(0x0d)
def op_load_immediate_byte(context):
    # fetch the next byte and put it in the register
    context.register = context.fetch()

# the "jump" opcode
# jumps to another place in program memory
# the argument is a 16 bit address (2 bytes, making this entire instruction 3 bytes long)
@op(0x0e)
def op_jump(context):
    # fetch the 16-bit address to jump to
    address = context.fetch_word()
    # and jump there!
    context.jump(address)

# the "wait a bit" opcode
# just for testing purposes, waits a second before continuing
@op(0x0f)
def op_wait(context):
    time.sleep(1)

# the "conditional jump" opcode
# this is just like the jump opcode, except...
# it only jumps if the value in the temporary register is truthy
# this is used to create "if" statements
# for example, load the value to be checked into the temporary register
# and then use this opcode to jump to the portion of code corresponding to "if true"
# otherwise, the jump will not happen, and the program will continue
# the code immediately following shoud be the "if false" code
# similarly, it can be used to create a loop that exits when some condition fails to be met
@op(0x10)
def op_jump_if(context):
    # fetch the 16-bit address to jump to
    address = context.fetch_word()
    # check the condition
    if context.register:
        # and jump there if it's truthy!
        context.jump(address)

