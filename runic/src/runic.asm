;;; the main entry point into the runic compiler!

; program entry
jmp main

; includes
#include variables.asm

#include util.asm

#include file_loader.asm

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
	echo @source_code%s

	; return with the result of compilation
	ret
