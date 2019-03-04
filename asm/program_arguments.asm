;;; test passing in arguments from the command line and stuff
; NOTE: expects all args to be NUMBERS

; they are passed in through the data stack
; so let's examine them
echo "here are the arguments given to this program:"
stackdump

; see how many arguments that is
stacklen @0
echo "that would be.... this many args...:"
echo @0

; lets convert those all to numbers
loop:
	echo "doing arg #..."
	echo @0

	; pull the arg
	pull @1%s
	echo @1%s ; see the raw string first

	; convert it from string to byte
	coerce @1, @1%s
	echo @1 ; and print that too

	; loop if not done
	dec @0
	jmpif @0, loop

;; some misc coerce tests
coerce @0%s, 10o
echo @0%s

; push a number AS A STRING
push "610"
; and pull it back, implicitly converting it to a WORD
pull @0%16
inc @0%16
echo @0%16

ret
