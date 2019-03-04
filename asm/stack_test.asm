;;; a test program for testing stack features
; the stack in the magic cpu is a completely separate memory region
; it's also not a linear sequence of bytes
; it's a python list lol
; address = index
; and data type is variable

; the stack at the begining of the program: (should be empty)
echo "here's the stack at the beginning:"
stackdump

; now push some random values to the stack:
push 1
push 2
push 3
push 50h
push 500
push "hello"
; also push a label address!
push secret_code

; and dump those
echo "have some stuff:"
stackdump

; and now, pull each thing off the stack and print it one by one
; pulling them onto ram address 0
; first that label address
pull @0%16
echo @0%16
stackdump
; also, before continuing, lets jump to that address just pulled from the stack!
jmp @0%16
return:
; then that string
pull @0%s
echo @0%s
stackdump
; and now a bunch of numbers
pull @0%16
echo @0%16
stackdump
pull @0
echo @0
stackdump
pull @0
echo @0
stackdump
pull @0
echo @0
stackdump
pull @0
echo @0
stackdump

; now lets test some function calls!!
echo "calling f1..."
call function_1
echo "calling f2..."
call function_2
echo "called all them functions"

; this would cause an error, because the call stack is empty:
;ret

; bye
halt 0

secret_code:
	echo "you've reached a secret portion of this program, goodbye"
	jmp return ; test

function_1:
	echo "this is function 1 speaking"
	ret

function_2:
	echo "this is function 2 speaking"
	; lets call another function inside this function!
	echo "calling f3 from inside f2..."
	call function_3
	echo "done calling f3! returning now"
	ret

function_3:
	echo "hello, this is the infamous f3."
	; evil
	ret
