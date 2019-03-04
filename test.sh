#!/usr/bin/env bash
# a script to quickly test and run assembly programs in asm/ and bin/

# asm file name
SOURCE=asm/$1.asm

# bin file name
BINARY=bin/$1.bin

# arguments
shift
ARGUMENTS="$@"

# assemble and run if successful
./assembler.py $SOURCE $BINARY && ./run.py $BINARY $ARGUMENTS
