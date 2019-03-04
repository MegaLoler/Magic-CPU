#!/usr/bin/env bash
# a script to quickly test and run assembly programs in asm/ and bin/

# asm file name
SOURCE=asm/$1.asm

# bin file name
BINARY=bin/$1.bin

# first assemble it
./assembler.py $SOURCE $BINARY

# then run it
./run.py $BINARY
