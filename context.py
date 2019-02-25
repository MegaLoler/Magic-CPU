# a context for the cpu to keep track of where it is in some memory
# for example, you would load program code into a context object like this
# and give it to the cpu to execute code from that memory
# also can tell the cpu who is running this program
# that way access can be had to the player's own local ram
class ExecutionContext:
    def __init__(self, memory, player, pointer=0):
        # memory is the bytes being accessed
        self.memory = memory
        # the player executing this program
        self.player = player
        # pointer is where the cpu is currently looking
        self.jump(pointer)
        # a temporary "register" for holding any temporary value
        # there'll be examples of what it's for
        self.register = None
        # this will tell whether the program has halted or not
        # when a program is finished and wants to exit, it will use the halt operation
        # which will then set this to True
        self.halted = False

    # set the pointer, wrapping it around if needed
    def jump(self, address):
        self.pointer = address % len(self.memory)

    # increment the pointer, but wrap around to the beginning if reached the end
    def next(self):
        self.jump(self.pointer + 1)

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
        return low_byte + high_byte * 2 ** 8
