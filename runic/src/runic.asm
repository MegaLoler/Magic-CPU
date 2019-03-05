;;; the main entry point into the runic compiler!

; program entry
jmp main

; includes
#include globals.asm
#include file_loader.asm
#include compile.asm

; main
; main(filename)
; filename = name of file on host system to compile
main:
	; greet the user
	echo "Welcome to the RUNIC compiler!"

	; load the file into ram
	; the filename argument is already on the stack,
	; so we can just call the function:
	; load_file(filename)
	call load_file

	; the source should now be returned as a string on the data stack
	; now compile it!
	; the result will be on the stack, ready to return with the main program
	call compile

	; return with the result of compilation
	ret
