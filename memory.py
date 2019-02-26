from abc import ABC

class MemoryInterface(ABC):
    ''' represents a memory interface from which you can read and to which you can write '''
    @abstractmethod
    def read(self, address, data_type):
        ''' read a value from this memory interface given some address to read from
        
        return the value itself as well as the address of the first byte after the read value'''
        ...

    @abstractmethod
    def write(self, address, value, data_type):
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
    def read(self, address, data_type):
        ''' read from the physical memory '''
        # TODO: data type
        post_address = address # TODO increment
        return self.contents[address], post_address

class RAM(ROM):
    ''' represents linear random access memory '''
    def write(self, address, value, data_type):
        ''' write a value to a location in this RAM '''
        # TODO: data type
        self.contents[address] = value
        return address # TODO increment

class FileMemory(ROM):
    ''' represents readonly access to the contents of a file '''
    # should mmap or load into ram?
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            # load the program from the file
            self.contents = f.read()
