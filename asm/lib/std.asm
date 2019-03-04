;;; a collection of useful code
;;; use in assembly files with the #include directive

; a function that prints a value with a prompt
; print_prompt(prompt, value)
print_prompt:
	; pop the prompt value
	pull @0%s
	; pop the value as well
	pull @80h%s
	; concatenate them
	cat @0%s, @80h%s
	; and echo it
	echo @0%s
	; bye
	ret
