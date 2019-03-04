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

push "arg"	; the data stack is a good means of passing argument and return values between functions
echo "calling f2..."
call function_2
pull @0%s
echo "f2 returned this value:"
echo @0%s

; done calling funcs!
echo "called all them functions"

; bye
; note, you can end a program either with the `halt` op
; or by using the `ret` op from the toplevel, such as here
ret

secret_code:
	echo "you've reached a secret portion of this program, goodbye"
	jmp return ; test

function_1:
	echo "this is function 1 speaking"
	ret

; let this function take one string argument given on the data stack
function_2:
	echo "this is function 2 speaking"
	; show the argument recieved
	echo "i've recieved this value:"
	pull @0%s
	echo @0%s
	
	; lets call another function inside this function!
	echo "calling f3 from inside f2..."
	call function_3
	echo "done calling f3! returning now"

	; let's return a message
	; py pushing it to the stack
	push "return value dude"
	ret

function_3:
	echo "hello, this is the infamous f3."
	; evil
	ret
