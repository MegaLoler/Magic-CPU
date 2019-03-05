;;; the main entry point into the runic compiler!

; program entry
jmp main

; includes
#include globals.asm
#include util.asm
#include file_loader.asm
#include compile.asm

; main
; main(filename)
; filename = name of file on host system to compile
main:
	; greet the user
	echo "Welcome to the RUNIC compiler!"

	; r0 = filename
	pull @r0%s
	push @r0%s

	; tell the user we are reading the file
	push "..."
	push @r0%s	; r0 = filename
	push "Loading file "
	push 3
	call print_cat

	; load the file into ram
	; the argument is already on the stack
	; load_file(filename)
	call load_file

	; the source should now be returned as a string on the data stack
	; now compile it!
	; the result will be on the stack, ready to return with the main program
	call compile

	; return with the result of compilation
	ret
