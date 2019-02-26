from abc import ABC

class MemoryInterfaceSpec(ABC):
    ''' represents a designator the different possible memory interfaces '''
    @abstractmethod
    def resolve(self, context):
        ''' get the actual memory interface for the context '''
        ...

class ProgramMemorySpec(MemoryInterfaceSpec):
    ''' represents a designator for program memory '''
    def resolve(self, context):
        ''' return program memory of this context '''
        return context.memory

class PlayerRAMSpec(MemoryInterfaceSpec):
    ''' represents a designator for player RAM '''
    def resolve(self, context):
        ''' return the executing player's ram '''
        return context.player.ram

class OmniRAMSpec(MemoryInterfaceSpec):
    ''' represents a designator for omnipresent RAM '''
    def resolve(self, context):
        ''' return the game instance's omni ram '''
        return context.game.ram
