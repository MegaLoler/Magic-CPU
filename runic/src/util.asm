;;; various useful functions

; concatenate a series of values and print the result
; print_cat(int length, *values)
print_cat:
	; do the concatenation first
	call multi_cat

	; now print the value
	pull @r0%s
	echo @r0%s

	; done
	ret

; concatenate a series of values and return the result
; multi_cat(int length, *values)
multi_cat:
	; the first argument is how many more arguments there are lol
	; r0 = length
	pull @r0

	; use r1 as scratch
	copy @r1%s, ""

	; accumulate the result at memory address 100
	_result=100
	copy @_result%s, ""	

	; iterate through the arguments and concat them
	loop:
		; grab the next value
		pull @r1%s

		; accumulate it
		cat @_result%s, @r1%s

		; loop
		dec @r0
		jmpif @r0, loop
	
	; return the result
	push @_result%s
	ret
