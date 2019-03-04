; here's some simple examples!


;;; HELLO
; programs always start executing from the beginning of program memory
; therefore, the entry point is right here:
; use the echo op to print the immediate value
echo "hello world!"


;;; LOOP
; now count down from 20!
; copy the value 100 into player ram location 0 as an 8 bit value
copy @0, 20
loop:
; and print the current value
echo @0
; and then decrement the value at location 0
dec @0
; and then keep looping if its not 0
jmpif @0, loop



;;; BAD OPCODE bc y not
; try to do something bad
;evil



;;; GREET THE USER!!
; lets make a lil message for the user
; store it at location 2 because why not
copy @2%s, "hey there "
; ask for the username
read @12%s, "whats ya naaaaaaaame bru? "
; now send them the message!!
echo @2%s
; wait for user acknowledgement
prompt "(press enter dude)"




;;; DO SOME MATH
; gonna use 16 bit numbers so they can be Bigga
echo "50 + 34 = "
copy @0%16, 50
add @0%16, 34
echo @0%16

echo "- 19 = "
sub @0%16, 19
echo @0%16

echo "* 7 = "
mul @0%16, 7
echo @0%16

echo "/ 6 = "
div @0%16, 6
echo @0%16

echo "% 4 = "
mod @0%16, 4
echo @0%16

echo "^ 7 = "
pow @0%16, 7
echo @0%16



;;; BITWISE STUFF
; negate an 8bit number
; before:
echo @0%8
; do it
neg @0%8
; after!:
echo @0%8




;;; OMNI RAM
; need to fix the grammar for it to work lol
;copy @o0%s, "string for omni ram!"
; tht string is now in OMNI ram rather than local player ram
;echo @o0%s


;;; access a string as the wrong type!
copy @1%s, "Hello"
; first, the right type
echo @1%s
; now as byte
echo @1%8
; or
echo @1
; now as word
echo @1%16


;;; use the cow opcode
prompt "are u ready to get cow'd up in here?"
cow
; check it out ; )
dump


;;; NUMBER BASES
; hex value 11
copy @0, 11h
; decimal value 11
;copy @2, 11d     ;;;;; BROKENNNNNNN hAAAAAAAA
; also decimal value 11
copy @4, 11
; octal value 11
copy @6, 11o
; binary value 100
;copy @8, 100b  ;;;;;; ALSO BROKEN AAAAAA
dump


; exit with a random value
halt 78
