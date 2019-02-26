# Magic CPU Example

Here is an example of a fantasy "CPU". It can have whatever functionality you want in how it is able to interact with the game world, the sky is the limit. It is able to access "omni-present ram" as well as individual players' ram. I provided examples of some very basic CPU functionality, such as reading and writing between different memories, and basic arithmetic and logical operations. I also tried to show some examples of "unorthodox" operations in an attempt to demonstrate how you can make the "CPU" able to interact with the game world in any way that you like.

There is a `run.py` script for testing out real programs on the CPU! This is just for demonstration purposes. Of course, in the actual game itself, you will be able to execute code provided by the players within the game itself.

# Examples

See the `bin` directory for a collection of pre-compiled programs that you can execute on the CPU!

In order to run one of the examples in a fake game environment for testing purposes, use the `run.py` script as follows:
```bash
python run.py bin/test.bin
```

Alternatively, you can write and compile your own binaries with the included `assembler.py` script like this:
```bash
python assembler.py asm/hello_world.asm bin/hello_world.bin
```

(You'll need to make sure you have the `tatsu` module installed in order to use the assembler.)
