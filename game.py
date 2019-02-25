class Game:
    ''' just a dummy class for representing a game instance where some omnipresent ram exists '''
    def __init__(self):
        self.ram = bytes(2**10*32) # 32kb of ram, of course it can be however much you like!

