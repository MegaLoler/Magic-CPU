#!/usr/bin/env bash
# script to reassmble all the example asm files into bin files

for asm in asm/*
do
	bin=bin/$(basename $asm .asm).bin
	./assembler.py $asm $bin
	if [ $? -ne 0 ]
	then
		break
	fi
done
