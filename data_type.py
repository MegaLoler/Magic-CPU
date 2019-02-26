from abc import *

# these are reader/writer interfaces for bytecode
# items encoded in the bytecode format are decoded with these interfaces using the read method
# and data to encoded are encoded with these intrefcase using the write method
# there is an interface for each primitive data type

# TODO: fix it so theres no danger of going out of bounds.... nicer than this

class DataTypeInterface(ABC):
    ''' represents a data type interface, with a bytestream reader and writer '''
    @abstractmethod
    def read(self, context, stream, address):
        ''' read a piece of data from a bytestream at address

        return the read data as well as the amount of bytes that were read
        '''
        ...

    @abstractmethod
    def write(self, context, stream, address, value):
        ''' write a piece of data into a bytestream at address

        return the amount of bytes that was written
        '''
        ...

class ByteInterface(DataTypeInterface):
    ''' represents the interface to an 8-bit quantity '''
    def read(self, context, stream, address):
        ''' read in a byte of data from a bytestream at address

        return the byte as well as the amount of bytes that were read
        '''
        return stream[address], 1

    def write(self, context, stream, address, value):
        ''' write a byte into a bytestream at some address

        return the amount of bytes that were written
        '''
        stream[address] = value % 2 ** 8
        return 1

    def compile(self, value):
        ''' compile a byte value into a bytecode representation '''
        return bytes([value])

class WordInterface(DataTypeInterface):
    ''' represents the interface to a 16-bit quantity '''
    def read(self, context, stream, address):
        ''' read in a 16-bit word of data from a bytestream at address

        return the value as well as the amount of bytes that were read
        '''
        # grab the low and high bytes separately
        # assuming low-endian byte order for now
        low_byte = stream[address]
        high_byte = stream[(address + 1) % len(stream)]
        # assemble the 16 bit value from the two parts
        value = low_byte + high_byte * 2 ** 8
        return value, 2

    def write(self, context, stream, address, value):
        ''' write a 16-bit word into a bytestream at some address

        return the amount of bytes that were written
        '''
        # disect the value into its high and low byte components
        # assuming low-endian byte order for now
        low_byte = value % 2 ** 8
        high_byte = value // 2 ** 8
        # and set both of those individual bytes in the stream
        stream[address] = low_byte
        stream[(address + 1) % len(stream)] = high_byte
        return 2

    def compile(self, value):
        ''' compile a word value into a bytecode representation '''
        # that means separate out the high and low bytes
        high_byte = value // 2 ** 8
        low_byte = value % 2 ** 8
        # remember, little-endian, so low byte first
        return bytes([low_byte, high_byte])

class StringInterface(DataTypeInterface):
    ''' represents a null terminate ascii encoded string '''
    def read(self, context, stream, address):
        ''' read a null terminated string from a byte stream at an address

        return the string as well as the amount of bytes that were read
        that means the length of the string itself + 1 because of the null terminating byte
        '''
        string = ''
        offset = 0
        # loop through the bytestream until encountering the null terminator (a 0)
        while True:
            # read the next byte
            byte = stream[(address + offset) % len(stream)]
            # keep track of the offset
            offset += 1
            # if its not a null terminator (0) then append it to the collected string value
            if byte: string += chr(byte)
            # otherwise we are done here
            else: break
        # return the string as well as the amount of bytes that were read
        return string, offset

    def write(self, context, stream, address, value):
        ''' write a null terminated string into the byte stream 

        return the amount of of bytes that were written
        '''
        # make sure this value is a string
        string = str(value)
        # and then get a bytestring of it
        data = string.encode()
        # add a null terminator
        data += bytes([0])
        # keep track of how many bytes are written
        offset = 0
        # loop through each byte in the byte string
        for byte in data:
            # write it into memory
            stream[(address + offset) % len(stream)] = byte
            # keep track of how many bytes have been written
            offset += 1
        # finally, return how many bytes were written
        return offset

    def compile(self, value):
        ''' complie a string value into a bytecode representation '''
        # encode it as ascii and add a null terminator
        return value.encode('ascii') + bytes([0])

class OpcodeInterface(DataTypeInterface):
    ''' an interface for encoding and decoding opcode byte values '''
    def read(self, context, stream, address):
        ''' decode an opcode from a stream

        bytecode format is just a number
        but if that numer is 0xff, then read the next byte and add 255
        the second byte can also be 0xff, meaning read the third byte and add 255 again
        and so on
        '''
        # keep track of how much data has been read
        offset = 0
        # store the opcode value
        opcode = 0
        # read until its not 0xff
        while True:
            # read the next byte
            byte = stream[address + offset]
            # keep track
            offset += 1
            # add the value
            opcode += byte
            # if it's 0xff, than means go to the next page of possible opcode values
            # otherwise we're done
            if byte != 0xff: break
        # return the opcode value and the amount of bytes read
        return opcode, offset

    def write(self, context, stream, address, value):
        # TODO
        pass

    def compile(self, value):
        ''' compile an opcode value as bytecode '''
        bytecode = bytes()
        while value >= 0xff:
            bytecode += bytes([0xff])
            value -= 0xff
        bytecode += bytes([value])
        return bytecode

class ImmediateInterface(DataTypeInterface):
    ''' interface for encoding and decoding immediate argument values from bytecode streams '''
    def __init__(self, data_type):
        self.data_type = data_type

    def read(self, context, stream, address):
        ''' read an immediate argument '''
        from argument import Immediate
        # use the data type interface of this immedate value, to read it
        value, offset = self.data_type.read(context, stream, address)
        # create an argument from this value
        argument = Immediate(value, self.data_type)
        # return the argument and the offset
        return argument, offset

    def write(self, context, stream, address, value):
        # TODO
        pass

class DirectInterface(DataTypeInterface):
    ''' interface for encoding and decoding direct address argument values from bytecode streams '''
    def __init__(self, memory_spec, data_type):
        self.memory_spec = memory_spec
        self.data_type = data_type

    def read(self, context, stream, address):
        ''' read a direct address argument '''
        from argument import Direct
        # read the address value (addresses are assumed to be 16 bit, so we use the word interface)
        address, offset = WordInterface().read(context, stream, address)
        # create an argument from this address value
        argument = Direct(context, self.memory_spec.resolve(context), address, self.data_type)
        # return the argument and the offset
        return argument, offset

    def write(self, context, stream, address, value):
        # TODO
        pass

# note: should probabably generalize this and the above, its much duplicate
class IndirectInterface(DataTypeInterface):
    ''' interface for encoding and decoding indirect address argument values from bytecode streams '''
    def __init__(self, memory_spec, data_type):
        self.memory_spec = memory_spec
        self.data_type = data_type

    def read(self, context, stream, address):
        ''' read an indirect address argument '''
        from argument import Indirect
        # read the address value (addresses are assumed to be 16 bit, so we use the word interface)
        address, offset = WordInterface().read(context, stream, address)
        # create an argument from this address value
        argument = Indirect(context, self.memory_spec.resolve(context), address, self.data_type)
        # return the argument and the offset
        return argument, offset

    def write(self, context, stream, address, value):
        # TODO
        pass

class InstructionInterface(DataTypeInterface):
    ''' represents an interface for reading and writing instruction encodings '''
    def read(self, context, stream, address):
        ''' decode an instruction from the bytecode stream '''
        from operation import opspecs, opcodes
        from instruction import Instruction
        # read the opcode first!
        opcode, offset = OpcodeInterface().read(context, stream, address)
        # look up the opspec for this opcode
        try:
            opspec = opspecs[opcode]
        except IndexError:
            opcode_string = format(opcode, '02x')
            address_string = format(address, '02x')
            raise Exception(f'Undefined opcode 0x{opcode_string} found at address 0x{address_string}')
        # this is a list
        # each item in the list is a data type interface for reading an argment
        # so loop through each, and use it to read an argument!
        # keep track of the arguments read
        arguments = list()
        for p in opspec:
            # read the argument
            argument, arg_offset = p.read(context, stream, address + offset)
            # keep track of offset
            offset += arg_offset
            # store the argument
            arguments.append(argument)
        # construct an instruction from these arguments
        # first get the operation
        operation = opcodes[opcode]
        # then construct the instruction
        instruction = Instruction(operation, arguments)
        # and return it and the total offset
        return instruction, offset

    def write(self, context, stream, address, value):
        # TODO
        pass

# primitive type singletons
byte_type = ByteInterface()
word_type = WordInterface()
string_type = StringInterface()
