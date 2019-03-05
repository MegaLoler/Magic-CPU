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

; read a single byte from a stream
; read_byte(stream *pointer)
read_byte:
	; r0 = stream pointer
	pull @r0%16
	
	; grab the current stream pointer address
	copy @r2%16, @@r0%16

	; grab a byte from the stream
	push @@r2

	; increment the stream pointer pointer
	inc @r2%16

	; and save it back as the stream pointer
	copy @@r0%16, @r2%16

	; return the byte
	ret
