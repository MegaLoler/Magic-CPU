;;; a test program for testing stack features
; the stack in the magic cpu is a completely separate memory region
; it's also not a linear sequence of bytes
; it's a python list lol
; address = index
; and data type is variable

; the stack at the begining of the program: (should be empty)
echo "here's the stack at the beginning:"
stackdump

loop:
; now push some random values to the stack:
push 1
push 2
push 3
push 50h
push 500
push "hello"
; also push a label address!
push loop

; and dump those
echo "have some stuff:"
stackdump

; and now, pull each thing off the stack and print it one by one
; pulling them onto ram address 0
; first that label address
pull @0%16
echo @0%16
stackdump
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

; bye
halt 0
