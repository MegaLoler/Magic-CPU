;;; the runic lexer

; tokenizes a code stream
; lex()
; works on the global source_code
; writes to the global token_string
lex:
	; make a stream from the source code
	push @source_code%16	; address of the text
	call make_stream

	; and make a stream for the token string as well
	push @token_string%16	; address of the token stream
	call make_stream
	swap	; put source on top of stack, token stream under it

	; clear the scratch buffer
	copy @buffer%s, ""

	; first eat white space
	call eat_white_space
	loop_:
		; loop through all the bytes and print them
		ppush
		call read_byte
		pull @r2%16	; r2 = 1 character string

		; print the byte
		;echo @r2%s
		;echo @r2

		; is it space?
		copy @r4, @r2
		sub @r4, 32
		jmpif @r4, next0
		; yes it is!
		echo "SPACE"
		jmp done
	next0:
		; is it newline?
		copy @r4, @r2
		sub @r4, 10
		jmpif @r4, next1
		; yes it is!
		echo "NEWLINE"
		jmp done
	next1:
		; is it tab?
		copy @r4, @r2
		sub @r4, 9
		jmpif @r4, next8
		; yes it is!
		echo "TAB"
		jmp done
	next8:
		; is it open paren?
		copy @r4, @r2
		sub @r4, 40
		jmpif @r4, next2
		; yes it is!
		echo "("
		jmp done
	next2:
		; is it close paren?
		copy @r4, @r2
		sub @r4, 41
		jmpif @r4, next3
		; yes it is!
		echo ")"
		jmp done
	next3:
		; is it open brace?
		copy @r4, @r2
		sub @r4, 123
		jmpif @r4, next4
		; yes it is!
		echo "{"
		jmp done
	next4:
		; is it close brace?
		copy @r4, @r2
		sub @r4, 125
		jmpif @r4, next5
		; yes it is!
		echo "}"
		jmp done
	next5:
		; is it semi colon?
		copy @r4, @r2
		sub @r4, 59
		jmpif @r4, next6
		; yes it is!
		echo ";"
		jmp done
	next6:
		; is it quote?
		copy @r4, @r2
		sub @r4, 34
		jmpif @r4, next7
		; yes it is!
		echo "QUOTE"
		jmp done
	next7:
		; stick it on the buffer
		cat @buffer%s, @r2%s
		jmp done2
	done:
		; tokenize this buffered string
		swap
		ppush
		call tokenize
		swap
		copy @buffer%s, ""
		call eat_white_space
	done2:
		
		; loop until null byte
		jmpif @r2, loop_

	; done
	ret

; put whats on the scratch buffer into the token stream
; tokenize(token_stream)
tokenize:
	leng @r0, @buffer%s
	jmpif @r0, doit
	pull 0
	ret
doit:
	push @buffer%s
	echo @buffer%s
	jmp write_string
