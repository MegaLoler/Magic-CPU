***Note:*** The first part of this document is all explanation of the basics. See the end of this document for a practical tutorial!

# RuneCore Basics

A program in RuneCore (magic assembly) is just a series of **instructions**. The program executes from the very top and goes downwards.

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

A direct argument in magic assembly is written as `@` followed by a number which is the memory address of the value.

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
; read: decrement [the value] at [memory location which is stored] at [memory location] 10
dec @@10
```

When using indirect addressing, as in the case of direct addressing, it is important to specify what type of data is located at that location in memory (see the below section on data types). By default, *byte* type is assumed.

### Data Types

There are (currently) three data types in magic assembly: **byte**, **word**, and **string**.

#### Byte

The *byte* in magic assembly is an *unsigned 8-bit value*, which means that it is an integer ranging from a minimum of `0` to a maximum of `255`.

A byte, of course, only occupies a single byte of space in memory, that byte being numerically equivalent to the value it represents.

A byte literal (for use as an immediate argument) is written as the number, followed by an optional *base designator*, followed by `%8`. For example, the *byte* value as written in hexidecimal `50` would be written as `50h%8`.

The *base designator* indicates what *base* the number is written in. The possible base designators are `b` (binary), `o` (octal), `d` (decimal, assumed by default if no base designator is present), and `h` (hexidecimal).

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

The *base designator* is the same as it is for bytes (see above section on bytes).

Note that number values less than `256` can be encoded as either a byte or a word. If you encode it is a word, however, it will occupy two bytes of memory, and the upper byte will be `0`.

When accessing a *word* using *direct addressing* or *indirect addressing*, postfix the memory address to be accessed with `%16` in order to specify that the value stored at that memory address is to be encoded and decoded from the bytestream as a *word* value that occupies two bytes of memory. For example, here is an instruction that reads an integer encoded as a *word* from memory (two bytes) at location `4` and prints it:
```asm
echo @4%16
```

#### String

The *string* in magic assembly is a *null-terminated sequence of ASCII character values*. This means that the sequence of characters making up the string is encoded into the bytestream as a sequence of bytes corresponding to the ASCII character codes for each character followed by a byte of `0` (the *null-terminator* (sounds cool lol)).

The amount of space that a string occupies in memory is always the character count + 1 (1 byte for each character + the null-terminator).

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
As a fun example, suppose you tried to access the string as a word. The first two bytes of the string (`72` and `101` in decimal, corresponding to the ASCII characters 'H' and 'e') would be fetched from memory and assembled into the integer `25928` because `72 + 101 * 256 = 25928`:
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

As mentioned, it isn't necessary to explicitely specify so when you want to access *player memory*, because it is the memory interface that is used by default. However, if you like, place an `r` before the number value which is the memory address to be accessed. Here is an example of an instruction that prints the number value located in player memory at location `14`, using the explicit syntax:
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

A label is defined on its own line by writing the *label name* followed by `:` like this: `[label name]:`
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

## The Stacks

**TODO: write about the data stack and the call stack**

# Practical Tutorial

Here are some examples of how to write familiar programming constructs in RuneCore.

## Arithmetic and Logic

The `add` operation takes two arguments, which can each be either a byte or a word, and sets the value of the first argument to be the result. This means that the first argument should be a place in memory, and not an immediate value.
```asm
; add 5 to the 16 bit value at memory address 7
add @7%16, 5
```

The `sub`, `mul`, `div`, `mod`, `pow`, `inc`, and `dec` operations work similarly.

As do the logical operations `band` (and), `bor` (or), `neg` (not), and `xor` (exclusive or)

## Conditional Branches

Use the `jmpif` operation to create an "if" statement. This operation takes one argument that is to be used as the condition, and a second argument that is the address to jump to (usually you will use a label). If the value is truthy, it will make the jump, otherwise it will not.

```asm
; test a byte value at memory location 5
jmpif @5, if_true
	; this marks the "else" branch
	echo "the value was falsey"

	; remember now to jump past the "if true" branch!
	jmp end_if

if_true:
	; this marks the "if true" branch
	echo "the value was truthy"

end_if:
; the program continues...
```

Sometimes you want to test for equality. To test if a value is equal to another value, subtract the value to compare it with. If the values are equal, the result will be 0, which is falsey, and otherwise the result will be greater than 0, which is truthy.

```asm
; check if the value in memory location 20 is 5
; first make a copy of the value to some scratch location, say location 0
copy @0, @20
; now subtract the value 5 to compare it with from the scratch copy
sub @0, 5
; now if it is NOT equal to 5, the result will be >0 (true)
; so jump to the "if false" or "else" branch if that is the case
jmpif @0, else_branch
	; the value in the scratch location was 0 (false)
	; that means the original value was equal to 5
	echo "yay, the value was indeed 5!"
	jmp end_if
else_branch:
	; they weren't equal, so the difference was not 0 (true)
	; and so the jump to this branch took place
	echo "aw, the value was not 5!"
end_if:
```

"else if" statements or "switch" statements can be written by nesting further "if" statements inside the "else" branch. Here is an example of a "switch" statement that checks if a value at memory location 2 is either 3, 40, 5, or 10:
```asm
; load the value to be checked into a scratch location
copy @0, @2
; check if it's 3
sub @0, 3
; if not, jump to the next test
jmpif @0, next1
	echo "it was equal to 3"
	jmp end
next1:
; do the next check, copy the value afresh
copy @0, @2
; check if it's 40
sub @0, 40
; if not, jump to the next test
jmpif @0, next2
	echo "it was equal to 40"
	jmp end
next2:
; do the next check, copy the value afresh
copy @0, @2
; check if it's 5
sub @0, 5
; if not, jump to the next test
jmpif @0, next3
	echo "it was equal to 5"
	jmp end
next3:
; do the last check, copy the value afresh
copy @0, @2
; check if it's 10
sub @0, 10
; if not, jump to the end
jmpif @0, end
	echo "it was equal to 10"
	; no need to jump now, because the end is right here!
end:
```

## Loops

To create a loop, use place a label at the start of the loop, and use the `jmp` and `jmpif` operations to jump from the end of the loop to the begining.

Here is an example of a simple infinite loop:
```asm
; mark the beginning of the loop
loop_start:
	; echo this forever
	echo "I am a loop."
	; and go back to the start of the loop
	jmp loop_start
```

Most of the time though you want to attach a condition to your loops. This is done exactly the same way as normal "if" statements, except you jump back to the condition at the end of the body of the loop.

Here is a "while" loop:
```asm
; let's make a while loop that loops 10 times
; let's use memory addres 8 to keep track of the counter
; initialize it at 10
copy @8, 10
; mark the beginning of the loop
loop_start:
	; this is the conditional part of the loop
	jmpif @8, loop_end

	; else, here is the body of the loop!
	echo "i'm looping so long as memory address 8 is not 0!"

	; decrement @8 until it reaches 0
	dec @8

	; loop!
	jmp loop_start
loop_end:
```

**TODO: show a "do while" loop where the condition is at the bottom, more efficient in some cases**

## Subroutines/Functions

Subroutines are essentially just pieces of code that get jumped to from various locations, and then jump back to the originating location when done. To jump back to the original location, it has to be kept track of, and this is done using the *call stack*. Use the `call` operation to jump to the subroutine and automatically push the return address onto the call stack. Use the `ret` operation to automatically pop the return address off of the call stack and jump back to that location.

```asm
; a function to greet people
greet:
	; say the message
	echo "hello there, how are you!"
	; go back to where you came from
	ret

; somewhere else in code....
; let's greet someone!
call greet
; let's greet them again!
call greet
; and again!
call greet
; lol
```

Many functions take arguments and return values. There are multiple ways of doing this. One way is to designate certain memory locations for use as arguments and return values. However, this doesn't scale well if those locations are fixed, and independant function calls could easily overwrite each other's values. Another way (which I recommend) is to use the *data stack* to pass arguments to functions and to return values from functions.

```asm
; a function to double a 16-bit number
; double(num) => num * 2
double:
	; grab the argument off the stack onto a temporary location
	pull @0%16

	; double it
	mul @0%16, 2

	; push the value to return back onto the stack
	push @0%16

	; and return!
	ret

; somewhere in the program...
; let's double a number several times!
; let's start with 3
copy @0%16, 3
echo @0%16

; double it
; pushing the argument to the function onto the stack
push @0%16
call double

; print the result
; pull the return value off the stack and print it
pull @0%16
echo @0%16

; double it again!
; pushing the argument to the function onto the stack again
push @0%16
call double

; print the result
; pull the return value off the stack and print it
pull @0%16
echo @0%16

; double it yet again!
; pushing the argument to the function onto the stack yet again
push @0%16
call double

; print the result
; pull the return value off the stack and print it
pull @0%16
echo @0%16
```

You can also have functions that accept multiple arguments and return multiple values by pushing multiple values to the stack as arguments or return values. Just be wary that you must push the arguments in the reverse order that they will be pulled, because the stack is a last-in-first-out structure!

**TODO: example of multiple argument functions and return values**

## Memory Management

How you make use of the stack and memory is up to you, but here are some recommendations.

Use the stack for all **local variables**. This way you can recursively call functions and the relevant data for that scope is always at the top of the stack as long as your stack remains balanced (you remember to pull everything you push).

Use memory for all **global variables**. Memory works great for global data because memory locations are fixed and can be accessed equally at any point in program execution.

Reserve the first 16 bytes or so of memory as **temporary registers**. These can be used to pass values to operations. Never rely on their contents being valid after a function call. Assume that any function you define may alter the contents of them. Push any data you need to save onto the stack before calling any functions, and then pop it back off when you are done.
