from abc import *
from data_type import *

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

    @property
    def value(self):
        return self.read()

    @value.setter
    def value(self, value):
        self.write(value)

class Literal(Argument):
    ''' represents a literal value as an argument '''
    def __init__(self, value):
        self.v = value

    def read(self):
        return self.v

    def write(self, value):
        pass # you can't write "to" a literal value lol

class Immediate(Literal):
    ''' represents an immediate value as an argument 
    
    same as Literal, in function, just a different name
    because it represent something slightly different '''

    def __init__(self, value, data_type):
        super().__init__(value)
        self.data_type = data_type

class Direct(Argument):
    ''' represents a value located in some memory at some address '''

    def __init__(self, context, memory, address, data_type):
        # address is the location in memory of the value
        self.context = context
        self.memory = memory
        self.address = address
        self.data_type = data_type

    def read(self):
        ''' read the value from the memory '''
        return self.memory.read(self.context, self.address, self.data_type)[0]

    def write(self, value):
        ''' write a value into the memory '''
        self.memory.write(self.context, self.address, value, self.data_type)

class Indirect(Argument):
    ''' represents a value located in some memory location specificed by some value in memory '''

    def __init__(self, context, memory, address, data_type):
        # address is the location in memory of the address of the value
        self.context = context
        self.memory = memory
        self.address = address
        self.data_type = data_type

    def read(self):
        ''' read the value in memory indicated by the value in memory '''
        address = self.memory.read(self.context, self.address, WordInterface())[0]
        return self.memory.read(self.context, address, self.data_type)[0]

    def write(self, value):
        ''' write a value to the address in memory specified at the address in memory '''
        address = self.memory.read(self.context, self.address, WordInterface())[0]
        self.memory.write(self.context, address, value, self.data_type)
