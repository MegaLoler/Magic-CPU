# this is just a dummy player class
# to show players having their own ram
class Player:
    def __init__(self):
        self.ram = bytes(2**10) # 1kb of ram, of course it can be however much you like!
