# Magic CPU Example

Here is an example of a fantasy "CPU". It can have whatever functionality you want in how it is able to interact with the game world, the sky is the limit. It is able to access "omni-present ram" as well as individual players' ram. I provided examples of some very basic CPU functionality, such as reading and writing between different memories, and basic arithmetic and logical operations. I also tried to show some examples of "unorthodox" operations in an attempt to demonstrate how you can make the "CPU" able to interact with the game world in any way that you like.

There is a `run.py` script for testing out real programs on the CPU! This is just for demonstration purposes. Of course, in the actual game itself, you will be able to execute code provided by the players within the game itself.

So far though, most of this is just the framework. I'd like to actually show more what you can do to expand it and do fancy high level things with it.

## Examples

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

To learn how to write code, see `tutorial.md`

## Ideas

I want to add built-in thread functionality. This would be easy: just a "new thread" operation, which spawns a new python thread with a copy of the execution context, and jumps to some location to continue executing from there.

I want to make instructions themselves first-class citizens. I think it wouldn't be too hard to do: there just needs to be a data type representing an instruction, and the code to encode and decode instructions to and from a bytestream is already available. Instructions themselves could be arguments to other instructions. Also consider evaluation order? And quoting! :D

I want to generalize the way data types work in such a way that you can define your own type specifications. Also, address range literals would be cool! And array/list literals would be cool.

I want there to be dynamically allocatable memories. An op code could dynamically allocate memory and provide a handle to interface with that memory. Addressing modes would natively be able to address arbitrary memory interfaces by handle.

In regards to both of the above, generalize the way the instruction arguments work even more, to be able to work with completely arbitrary data types, memory interfaces, and addressing modes.

Speaking of addressing modes, generalize indirection such that you can have an arbitrary amount of layers of references! (The syntax would reflect this by allowing you to have any number of `@` prefixes)

Cons cells would make a really nice built in data type ; )

## Todo

Implement the above ideas! And reworking whatever underlying code necessary in the process, haha.

Fix the grammar so that memory interface designation actually works. XD

Local labels are good

Honestly just clean up a lot of the code in general, lol, there's a lot of slop

Reconsider instruction encodings! Should all possible instructions, resulting from all the combinations of operations, addressing modes, memory interfaces, and type specifications, be allocated explicitely to whatever opcode values are available like it is right now? Or should there be more of a system?

Also figure out a way to more cleanly specify the nature of acceptible arguments to operations -- including specifying which arguments are optional!

A lot of other stuff I can't think of right now
