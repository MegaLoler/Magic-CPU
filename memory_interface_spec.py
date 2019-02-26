from abc import *

# i wonder if this whole thing shouldn't be rewritten as just functions and not bother with classes

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

# singletons
program_memory_spec = ProgramMemorySpec()
player_ram_spec = PlayerRAMSpec()
omni_ram_spec = OmniRAMSpec()

# tuple
memory_interface_specs = program_memory_spec, player_ram_spec, omni_ram_spec
