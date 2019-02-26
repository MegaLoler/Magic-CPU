from abc import ABC

class DataTypeInterface(ABC):
    ''' represents a data type interface, with a bytestream reader and writer '''
    @abstractmethod
    def read(self, stream, address):
        ''' read a piece of data from a bytestream at address

        return the read data as well as the amount of bytes that were read
        '''
        ...

    @abstractmethod
    def write(self, stream, address, value):
        ''' write a piece of data into a bytestream at address

        return the amount of bytes that was written
        '''
        ...

class ByteInterface(DataTypeInterface):
    ''' represents the interface to an 8-bit quantity '''
    def read(self, stream, address):
        ''' read in a byte of data from a bytestream at address

        return the byte as well as the amount of bytes that were read
        '''
        return stream[address], 1

    def write(self, stream, address, value):
        ''' write a byte into a bytestream at some address

        return the amount of bytes that were written
        '''
        stream[address] = value
        return 1

class WordInterface(DataTypeInterface):
    ''' represents the interface to a 16-bit quantity '''
    def read(self, stream, address):
        ''' read in a 16-bit word of data from a bytestream at address

        return the value as well as the amount of bytes that were read
        '''
        # grab the low and high bytes separately
        # assuming low-endian byte order for now
        low_byte = stream[address]
        high_byte = stream[address + 1]
        # assemble the 16 bit value from the two parts
        value = low_byte + high_byte * 2 ** 8
        return value, 2

    def write(self, stream, address, value):
        ''' write a 16-bit word into a bytestream at some address

        return the amount of bytes that were written
        '''
        # disect the value into its high and low byte components
        # assuming low-endian byte order for now
        low_byte = value % 2 ** 8
        high_byte = value // 2 ** 8
        # and set both of those individual bytes in the stream
        stream[address] = low_byte
        stream[address + 1] = high_byte
        return 2

class StringInterface(DataTypeInterface):
    ''' represents a null terminate ascii encoded string '''
    def read(self, stream, address):
        ''' read a null terminated string from a byte stream at an address

        return the string as well as the amount of bytes that were read
        that means the length of the string itself + 1 because of the null terminating byte
        '''
        string = ''
        offset = 0
        # loop through the bytestream until encountering the null terminator (a 0)
        while True:
            # read the next byte
            byte = stream[address + offset]
            # keep track of the offset
            offset += 1
            # if its not a null terminator (0) then append it to the collected string value
            if byte: string += byte.decode()
            # otherwise we are done here
            else: break
        # return the string as well as the amount of bytes that were read
        return string, offset

    def write(self, stream, address, value):
        ''' write a null terminated string into the byte stream 

        return the amount of of bytes that were written '''
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
            stream[address + offset] = byte
            # keep track of how many bytes have been written
            offset += 1
        # finally, return how many bytes were written
        return offset
