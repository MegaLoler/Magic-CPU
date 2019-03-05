#!/usr/bin/env bash
# script to reassmble all the example asm files into bin files

for asm in asm/*.asm
do
	bin=bin/$(basename $asm .asm).rune
	./assembler.py $asm $bin
	if [ $? -ne 0 ]
	then
		break
	fi
done
