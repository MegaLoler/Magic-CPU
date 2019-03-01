# Magic Assembly Tutorial

A program in magic assembly is just a series of **instructions**. The program executes from the very top and goes downwards.

**Comments** start with a `;`.

A **label** is a name followed by a `:` and is used to mark places in the code (examples later).

## Instructions

Each instruction is written on its own line and looks like this: `[mnemonic] [optional comma separate list of arguments]`

Here are some examples of the format with different numbers of arguments:
```asm
mnemonic                                 ; no arguments
mnemonic argument1                       ; one argument
mnemonic argument1, argument2            ; two arguments
mnemonic argument1, argument2, argument3 ; three arguments
mnemonic argument1,argument2             ; whitespace between arguments are optional
mnemonic argument1,       argument2      ; ditto!
```

The **mnemonic** is the *name* of the *operation* to perform. An **operation** is like a *function* that is built into the CPU.

This is an example of an *instruction* that prints `Hello` using the `echo` *operation*:
```asm
echo "Hello"
```

## Arguments

An argument in magic assembly has two basic attributes: **addressing mode** and **data type**.

In short, the addressing mode is where the value of the argument is to be found, and the data type is what kind of data it is (obviously, lol).

### Addressing Modes

In magic assembly, there are (currently) three kinds of addressing modes: **Immediate**, **Direct**, and **Indirect**.

#### Immediate Arguments

An immediate argument is a *literal* value. It is called *immediate* because the raw value is encoded into the bytecode immediately following the opcode rather than being located somewhere else in memory.

Here, an *immediate string* argument is given to the `echo` operation:
```asm
echo "I am an immediate value!"
```

#### Direct Arguments

A direct argument is an argument whose value is located somewhere else in memory. It is like an *unnamed variable*, that is, a variable addressed by *memory address* rather than name.

A direct argument in magic assembly is written as '@' followed by a number which is the memory address of the value.

Here is an example of an instruction that increments the number stored at memory location `50` by 1 using the `inc` operation:
```asm
; read: increment [the value] at [memory location] 50
inc @50
```

When using direct addressing, it is important to specify what type of data is located at that location in memory (see the below section on data types). By default, *byte* type is assumed.

#### Indirect Arguments

An indirect argument is slightly more advanced. Its value is stored at a location in memory which is also specified in memory. For example, if the actual value is stored at memory location `10`, the value `10` might be stored in memory location `5`. This addressing mode is used in situations when you may not know the exact location of a value you want to access until runtime.

An indirect argument in magic assembly is written as `@@` followed by the number which is the memory address of the value which specifies the memory address of the value of the argument (whew!).

Here is an example of an instruction that decrements the number stored at memory location `50`, assuming that the value `50` is stored at memory location `10`:
```asm
read: decrement [the value] at [memory location which is stored] at [memory location] 10
dec @@10
```

When using indirect addressing, as in the case of direct addressing, it is important to specify what type of data is located at that location in memory (see the below section on data types). By default, *byte* type is assumed.

### Data Types

There are (currently) three data types in magic assembly: **byte**, **word**, and **string**.

#### Byte

The *byte* in magic assembly is an *unsigned 8-bit value*, which means that it is an integer ranging from a minimum of `0` to a maximum of `255`.

A byte, of course, only occupies a single byte of space in memory, that byte being numerically equivalent to the value it represents.

A byte literal (for use as an immediate argument) is written as the number, followed by an optional *base designator*, followed by `%8`. For example, the *byte* value as written in hexidecimal `50` would be written as `50h%8`.

When accessing a *byte* using *direct addressing* or *indirect addressing*, postfix the memory address to be accessed with `%8` in order to specify that the value stored at that memory address is to be encoded and decoded from the bytestream as a *byte* value that occupies a single byte of memory. (Note that this is not explicitely necessary in the case of *byte* values, because *byte* is assumed by default.) For example, here is an instruction that reads an integer encoded as a *byte* (one byte) from memory at location `300` and prints it:
```asm
echo @300%8
```

#### Word

The *word* in magic assembly is an *unsigned 16-bit value*, which means that it is an integer ranging from a minimum of `0` to a maximum of `65536`.

A word occupies two bytes of space in memory. The **byte order** of the magic CPU is **little-endian**, which means that number values composed of multiple bytes are arranged in order of *increasing significance*. This means that the first byte of a *word* value represents the *least significant digits*, and the second byte represents the *most significant digits*.

Mathematically, the first byte is equivalent to `value % 256` and the second byte is equivalent to `value // 256` (integer division). For example, the number `2468` would be encoded into the bytestream as a word such that the first byte is `164` and the second byte is `9`. This is because `2468 = 164 + 9 * 256`.

If all of this is confusing to think about, don't worry! It is much easier to understand using hexidecimal numbers. For example, the number written in hexidecimal `a74c` would be encoded into the bytestream as a word such that the first byte is `4c` and the second byte is `a7`.

A word literal (for use as an immediate argument) is written as the number, followed by an optional *base designator*, (optionally) followed by `%16`. For example, the *word* value as written in octal `4711` would be written as `4711o%16`. Note that number literals are interpretted as word values by default, so that it's not strictly necessary to append `%16` to the value. For example, the word value as written in decimal, `1234` can simply be written as `1234`.

Note that number values less than `256` can be encoded as either a byte or a word. If you encode it is a word, however, it will occupy two bytes of memory, and the upper byte will be `0`.

When accessing a *word* using *direct addressing* or *indirect addressing*, postfix the memory address to be accessed with `%16` in order to specify that the value stored at that memory address is to be encoded and decoded from the bytestream as a *word* value that occupies two bytes of memory. For example, here is an instruction that reads an integer encoded as a *word* from memory (two bytes) at location `4` and prints it:
```asm
echo @4%16
```

#### String

The *string* in magic assembly is a *null-terminated sequence of ASCII character values*. This means that each character is encoded into the bytestream as a sequence of bytes corresponding to the ASCII character codes for each character followed by a byte of `0` (the *null-terminator* (sounds cool lol)).

The amount of that a string occupies in memory is always the character count + 1 (1 byte for each character + the null-terminator).

For example, the string `Hello` would be encoded into the bytestream as the following sequence of bytes (in hexidecimal): `48 65 6c 6c 6f 00`

A string literal (for use as an immediate argument) is simply the string encosed between `"` and `"`. For example, the string value `Goodbye` would be written as `"Goodbye"`.

When accessing a *string* using *direct addressing* or *indirect addressing*, postfix the memory address to be accessed with `%s` in order to specify that the value stored at that memory address is to be encoded and decoded from the bytestream as a *string* value that is terminated by a null byte. For example, here is an instruction that reads a string from memory starting at location `60` and prints it:
```asm
echo @60%s
```
In order to stress the importance of specifying the type of the data being accessed in memory, consider a situation in which the string `Hello` is encoded in memory at location `1`, and you want to print it to the screen using the `echo` operation. Suppose you forget to specify that the data stored at that location in memory is a string. By default, the assembler will assume you are trying to access a *byte*, and thus, the first byte of the string will be read, and printed onto the screen as the number `72` (which is the ASCII value for `H`):
```asm
; assuming the string "Hello" is at memory location 1:
echo @1
; => 72
```
As a fun example, suppose you tried to access the string as a word. The first two byte of the string (`72` and `101` in decimal, corresponding to the ASCII characters 'H' and 'e') would be fetched from memory and assembled into the integer `25928` because `72 + 101 * 256 = 25928`:
```asm
; assuming the string "Hello" is at memory location 1:
echo @1%16
; => 25928
```

### Memory Interfaces

_**NOTE:** The grammar for specifying alterate memory interfaces is currently broken!_

In magic assembly, the memory interface is a third attribute of arguments that only applies to *direct* and *indirect* arguments. The memory interface specifies which memory interface to access.

There are (currently) three memory interfaces: **program memory**, **player RAM**, and **omni-present RAM**.

The *program memory* is a *read-only* memory that contains the program bytecode currently being executed by the magic CPU.

The *player RAM* is a (currently 1kb) block of *read-write* memory that is local to every player running their own programs. A direct or indirect argument refers by default to the player RAM unless another memory inteface is specified.

The *omni-present RAM* is a (currently 4kb) block of *read-write* memory that is accessible uniformly by any player running any program.

In order to access *program memory*, place a `p` before the number value which is the memory address to be accessed. Here is an example of an instruction that prints the number value located in program memory at location `20`:
```asm
; read: echo [the value] at program memory location 20
echo @p20
```

As mentioned, it isn't necessary to explicitely specify so when you want to access *player memory*, becaues it is the memory interface that is used by default. However, if you like, place an `r` before the number value which is the memory address to be accessed. Here is an example of an instruction that prints the number value located in player memory at location `14`, using the explicit syntax:
```asm
; read: echo [the value] at [player] ram location 14
echo @r14
```

Lastly, *omni-present memory* is similarly accessed using an `o` before the number value which is the memory address to be accessed:
```asm
; read: echo [the value] at omni-present ram location 500
echo @o100
```

## Labels

**Labels** are a way of marking locations in the program memory. This is useful if you want to **jump** to a portion of code. Once a label is defined, it can be used in the place of any *memory address* or *word literal* in an argument.

A label is defined on its own line by writing the *label name* followed by `:` like this:
```asm
[label name]:
```
For example, this is how you would define a label called `sup`:
```asm
sup:
```

As an example of a simple use for a label, here is a small program that prints `Hello` first, and then *loops* forever printing `world`:
```asm
; first print Hello
echo "Hello"
; this label marks the begining of the loop
loop:
; print world
echo "world"
; and jump back to the beginning of the loop, repeating forever
jmp loop
```
