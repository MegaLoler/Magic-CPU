# Magic CPU Example

Here is an example of a fantasy "CPU". It can have whatever functionality you want in how it is able to interact with the game world, the sky is the limit. It is able to access "omni-present ram" as well as individual players' ram. I provided examples of some very basic CPU functionality, such as reading and writing between different memories, and basic arithmetic and logical operations. I also tried to show some examples of "unorthodox" operations in an attempt to demonstrate how you can make the "CPU" able to interact with the game world in any way that you like.

There is a `run.py` script for testing out real programs on the CPU! This is just for demonstration purposes. Of course, in the actual game itself, you will be able to execute code provided by the players within the game itself.

## Files

`cpu.py` contains the `CPU` class which represents the fantasy "CPU" itself. All of the CPU's operations are defined per opcode. In order to use a CPU, first instantiate it with the game instance (so that it is able to access the game's omni-present ram, provide an execution context (see below) containing information about the program to be executed as well as who is executing it, and then call the `step` method in order to step through the actual execution of the program.

`context.py` contains an `ExecutionContext` class. When a player wants to run a program using a "CPU", you can create an execution context to hold the memory that holds the program to be run (program memory) as well as a reference to the player running the program, which enables the "CPU" to access the player's local ram.

`player.py` contains a dummy `Player` class containing player-local ram. You don't need to use this class in the actual game, it's just for demonstrating how you can make your own Player class have its own ram.

`game.py` contains a dummy `Game` class containing "omni-present" ram for an instance of a game. You also don't need to use this class in the actual game, it's just for demonstrating omni-present ram.

`run.py` is a script for testing programs in a dummy game environment (see below).

# Examples

See the `bin` directory for a collection of pre-compiled programs that you can execute on the CPU!

In order to run one of the examples in a fake game environment for testing purposes, use the `run.py` script as follows:
```bash
python run.py bin/test.bin
```
