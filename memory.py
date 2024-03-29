from abc import *

class MemoryInterface(ABC):
    ''' represents a memory interface from which you can read and to which you can write '''
    @abstractmethod
    def read(self, context, address, data_type):
        ''' read a value from this memory interface given some address to read from
        
        return the value itself as well as the address of the first byte after the read value'''
        ...

    @abstractmethod
    def write(self, context, address, value, data_type):
        ''' write a value to some address using this memory interface

        return the address the first byte after the written value
        '''
        ...

    @property
    @abstractmethod
    def length(self):
        ''' get how many bytes are addressable using this interface '''
        ...

class PhysicalMemory(MemoryInterface):
    ''' represents a linear arrangement of real memory '''
    def __init__(self, contents):
        # contents is a bytes string
        self.contents = contents

    @property
    def length(self):
        ''' get the length of the linear contents '''
        return len(self.contents)

class ROM(PhysicalMemory):
    ''' represents a read only physical memory '''
    def read(self, context, address, data_type):
        ''' read from the physical memory '''
        value, length = data_type.read(context, self.contents, address)
        return value, address + length

    def write(self, context, address, value, data_type):
        ''' can't write to rom! '''
        pass

class RAM(ROM):
    ''' represents linear random access memory '''
    def write(self, context, address, value, data_type):
        ''' write a value to a location in this RAM '''
        length = data_type.write(context, self.contents, address, value)
        return address + length

class FileMemory(ROM):
    ''' represents readonly access to the contents of a file '''
    # should mmap or load into ram?
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            # load the program from the file
            self.contents = f.read()
