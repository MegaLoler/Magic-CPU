from enum import Enum
from abc import ABC
from data_type import DataType

class Argument(ABC):
    ''' represents an argument to an instruction

    an instruction argument designates a value to be resolved at the time of executing that instruction
    '''
    @abstractmethod
    def read(self):
        ''' read the value that this argument represents at runtime in an execution context '''
        ...

    @abstractmethod
    def write(self, value):
        ''' write a value to a location represented by this argument at runtime '''
        ...

    def __get__(self):
        ''' get the value of this argument '''
        return self.read()

    def __set__(self, value):
        ''' set the value of this argument '''
        self.write(self, value)

class Literal(Argument):
    ''' represents a literal value as an argument '''
    def __init__(self, value):
        self.value = value

    def read(self):
        return self.value

class Immediate(Literal):
    ''' represents an immediate value as an argument '''
    def __init__(self, context, data_type):
        # fetch the value from the execution context, program memory
        self.value = context.fetch(data_type)

class Direct(Argument):
    ''' represents a value located in some memory at some address '''
    def __init__(self, memory, address, data_type):
        self.memory = memory
        self.address = address
        self.data_type = data_type

    def read(self):
        ''' read the value from the memory '''
        return self.memory.read(self.address, self.data_type)[0]

    def write(self, value):
        ''' write a value into the memory '''
        self.memory.write(self.address, value, self.data_type)

class Indirect(Argument):
    ''' represents a value located in some memory location specificed by some value in memory '''
    def __init__(self, memory, address, data_type):
        # address is the location in memory of the address of the value
        self.memory = memory
        self.address = address
        self.data_type = data_type

    def read(self):
        ''' read the value in memory indicated by the value in memory '''
        address = self.memory.read(self.address, DataType.WORD)
        return self.memory.read(address, self.data_type)[0]

    def write(self, value):
        ''' write a value to the address in memory specified at the address in memory '''
        address = self.memory.read(self.address, DataType.WORD)
        self.memory.write(address, value, self.data_type)
