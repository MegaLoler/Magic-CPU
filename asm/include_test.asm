;;; example of a program that uses external files

; the entry point
jmp main

; include external code
#include lib/std.asm

; example of a null preprocessor directive
#nop

main:
	; use the external 'print with prompt' function
	read @0%s, "what's your name? "
	push @0%s
	push "your name is "
	call print
	ret	
