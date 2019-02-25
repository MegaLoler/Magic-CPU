class DataType(Enum):
    ''' represents the different data types
    
    data type is what kind of data it is, obviously, haha, and is any of the following:
    - byte (8 bit value)
    - word (16 bit value)
    - string (a series of ascii encoded characters terminated with a null byte (= 0))
    obviously subject to change and/or expansion
    '''
    BYTE = 1
    WORD = 2
    STRING = 3
