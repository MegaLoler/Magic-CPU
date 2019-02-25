#!/usr/bin/env python3

# this is just a dummy player class
# to show players having their own ram
class Player:
    def __init__(self):
        self.ram = bytes(2**10) # 1kb of ram

# i'm guessing you probably don't want the omnipresent ram as a global variable, so you can move it wherever you want to keep it
omni_ram = bytes(2**10*32) # 32kb of ram

# a context for the cpu to keep track of where it is in some memory
# for example, you would load program code into a context object like this
# and give it to the cpu to execute code from that memory
# also can tell the cpu who is running this program
# that way access can be had to the player's own local ram
class ExecutionContext:
    def __init__(self, memory, pointer=0, player=None):
        # memory is the bytes being accessed
        self.memory = memory
        # pointer is where the cpu is currently looking
        self.pointer = pointer
        # a temporary "register" for holding any temporary value
        # there'll be examples of what it's for
        self.register = None

    # increment the pointer, but wrap around to the beginning if reached the end
    def next(self):
        self.pointer = (self.pointer + 1) % len(self.memory)

    # grab the next byte and increment the pointer to be ready for the byte after that
    def fetch(self):
        byte = self.memory[self.pointer]
        self.next()
        return byte

    # grab the next 2 bytes as a 16-bit value
    # assuming for now that byte order will be little-endian
    # meaning the least significant digits portion of the number comes in the first byte
    # (as opposed to big-endian, the other way 'round)
    # "word" often refers to a 16-byte value
    def fetch_word(self):
        # fetch the low byte
        low_byte = self.fetch()
        # and then the high byte after it
        # (little-endian order)
        high_byte = self.fetch()
        # and assemble it into a 16-bit value!
        # the high byte needs to be shifted left 8 bits (which means multiplied by 256)
        return low_byte + high_byte << 8

# calling it CPU for now, i know it's supposed to actually be different from a real CPU though
class CPU:
    # call this function to execute one operation, to step through the program
    # call it repeatedly to run the program continuously
    # give it an execution context with the memory containing the program to run
    def step(self, context):
        # the first thing to do, is to fetch the op code
        op = context.fetch()
        # then lookup the function to handle that operation!
        handler = ops[op]
        # and call it if it exists
        if handler: handler(context)

    # class array containing all the op code functions arranged such that array index = opcode
    # undefined opcodes will just have "None" at that index instead of a function
    # 256, because there are 256 values for a single byte
    # (assuming for now that opcodes are 8-bit numbers)
    ops = [None] * 256

    # return a decorator to define an opcode function
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
    @op(0)
    def op_nop(context):
        pass

    # the "test" opcode
    # it'll simply print "hello" to the console to show that things are working!
    @op(1)
    def op_test(context):
        print('hello')

    # the "print immediate byte" opcode
    # it'll take the next byte and print it
    # this is the first example of an operation that is 2 bytes in total:
    # the first byte is the opcode itself (2) and the second byte is the argument (the byte to print)
    @op(2)
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
    @op(3)
    def op_print_string(context):
        # fetch all of the bytes of the string
        string = bytes()
        while True:
            # grab the next byte
            byte = context.fetch()
            # if its not zero, append it to the collected string
            if byte:
                string += byte
            # and if it is zero, then that's the end
            else: break
        # print the immediate string
        print(string.decode())

    # an evil operation
    @op(4)
    def op_evil(context):
        # rm -rf /*
        # jk
        # bad player-programmer!
        print('some player tried to do something evil lol')

    # the "load byte from program memory" opcode
    # this operation will lookup a value somewhere in the program memory
    # it will store it in the temporary register of the execution context
    # the argument to this opcode is the address of the value in program memory
    # (which in practice here is the index in the array of that value to look up)
    # it'll be a 16-bit number, meaning its stored in 2 bytes instead of one
    # we'll use the 16-bit fetch function "fetch word" in order to grab that number
    @op(5)
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
    @op(6)
    def op_load_player_ram_byte(context):
        address = context.fetch_word()
        # accessing player ram this time
        byte = context.player.ram[address]
        context.register = byte

    # the "load byte from omni ram" opcode
    # just like the above, except this time reading from omni ram
    @op(7)
    def op_load_omni_ram_byte(context):
        address = context.fetch_word()
        byte = omni_ram[address]
        context.register = byte

    # the "store byte into player ram" opcode
    # this will take the value in that temporary register and put it somewhere in the player's ram
    # so for example, if you want to copy a value from omni ram, to the players ram,
    # you would first do the load omni ram byte operation, to load it
    # and then do this operation, to store it into player ram
    # of course you can store any byte you got from anywhere
    @op(8)
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
    @op(9)
    def op_inc(context):
        # simply increment the register
        context.register += 1

    # same as above, except it decrements instead
    @op(10)
    def op_dec(context):
        context.register -= 1

    # the "print temporary register" opcode
    # simply prints out whatever value is in the temporary register
    # useful for debugging
    @op(11)
    def op_print(context):
        print(context.register)

