;;; some string manipulation tests!

; simply print a string
echo "hello there"

; store a string in memory
copy @0%s, "i am in memory m8"
echo @0%s	; and print it of course

; append something onto that string
cat @0%s, " and there's nothing you can do about it muahuahahah"
echo @0%s

; lets try out the "print with prompt" function!
; always push the last arguments first
push 500			; push the value
push "this is a number: "	; and the prompt
call print

; bye
echo "that is all folks"
ret

; a function that prints a value with a prompt
; print(prompt, value)
print:
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
