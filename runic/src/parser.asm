;;; the runic parser

#include stream.asm

; parses code text into an ast
; parse(code)
parse:
	; make a stream from the source code
	push @source_code%16	; address of the text
	call make_stream

	loop_:
		; r0 = stream pointer
		pull @r0%16
		push @r0%16

		; loop through all the bytes and print them
		push @r0%16
		call read_byte
		pull @r2	; r2 = byte

		; print the byte
		echo @r2
		
		; loop until null byte
		jmpif @r2, loop_

	; pull off and discard the stream pointer
	pull 0

	; done
	ret
