;;; the main entry point into the runic compiler!

; program entry
jmp main

; includes
#include globals.asm
#include memory.asm
#include util.asm
#include file_loader.asm
#include compile.asm

; main
; main(filename)
; filename = name of file on host system to compile
main:
	; greet the user
	echo "Welcome to the RUNIC compiler!"

	; init memory and globals
	call init

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
	echo @@source_code%s	; tmp
	
	; return with the result of compilation
	ret

; initialize memory and global variables
init:
	; setup memory management
	call init_mem

	; allocate memory for the scratch buffer
	push 100h	; 256 bytes for now ?
	call alloc
	; set global scratch buffer pointer to allocated mem
	pull @buffer%16		; pointer
	pull 0			; discard allocated byte size

	; allocate memory for the source code
	push 400h	; 1kb for now ?
	call alloc
	; set global source code pointer to allocated mem
	pull @source_code%16	; pointer
	pull 0			; discard allocated byte size

	; allocate memory for the token stream
	push 200h	; .5kb for now ?
	call alloc
	; set global token stream pointer to allocated mem
	pull @token_string%16	; pointer
	pull 0			; discard allocated byte size

	; done
	ret
