;;; interface to handle streams of data
; a stream is read from left to right

; make a stream from a pointer to a string
; make_stream(string *pointer)
make_stream:
	; allocate memory for the stream pointer
	push 2	; 2 bytes for the pointer
	call alloc
	pull @r2%16	; r2 = stream pointer pointer
	pull 0		; discard bytes	

	; point the stream pointer to the beginning of the string
	; r0 = pointer to string
	pull @r0%16
	copy @@r2%16, @r0%16

	; retur nthe stream pointer
	push @r2%16
	ret

; skip over a byte in the stream
; skip_byte(stream *pointer)
skip_byte:
	; r0 = stream pointer
	pull @r0%16
	
	; grab the current stream pointer address
	copy @r2%16, @@r0%16

	; increment the stream pointer pointer
	inc @r2%16

	; and save it back as the stream pointer
	copy @@r0%16, @r2%16

	; done
	ret

; read a single byte from a stream but do NOT increment the pointer!
; peek_byte(stream *pointer)
peek_byte:
	; r0 = stream pointer
	pull @r0%16
	
	; grab the current stream pointer address
	copy @r2%16, @@r0%16

	; grab a byte from the stream
	push @@r2

	; return the byte
	ret

; read a single byte from a stream
; read_byte(stream *pointer)
read_byte:
	; grab a byte from the stream
	call peek_byte

	; increment the stream pointer pointer
	inc @r2%16

	; and save it back as the stream pointer
	copy @@r0%16, @r2%16

	; return the byte
	ret

; write a byte to a stream
; write_byte(byte byte, stream *pointer)
write_byte:
	; TODO
	pull 0
	pull 0
	ret

; write a string to a stream
; write_string(string string, stream *pointer)
write_string:
	pull @r4%s		; r4 = string
	pull @r0%16		; r0 = stream pointer
	copy @r2%16, @@r0%16	; r2 = tail pointer
	copy @@r2%s, @r4%s
	leng @r4%16, @r4%s	; r4 = string length
	add @r2%16, @r4%16	; increment tail pointer
	inc @r2%16		; account for null terminator
	copy @@r0%16, @r2%16	; save it back
	ret

; consume white space in a stream
; eat_white_space(stream *pointer)
; returns the stream pointer
eat_white_space:
	; need to remove space (32) and newline (10)
	; and TODO: tab and carriage return
	loop__:
		; see what the next byte is
		ppush
		call peek_byte	
		pull @r2	; r2 = byte

		; is it space?
		copy @r3, @r2
		sub @r3, 32
		jmpif @r3, nope
		jmp yep
	nope:
		; is it newline?
		copy @r3, @r2
		sub @r3, 10
		jmpif @r3, nope2
	yep:

		; ok then eat it and loop
		; r0 = stream pointer
		ppush
		call skip_byte
		jmp loop__
	
nope2:
	; done
	ret
