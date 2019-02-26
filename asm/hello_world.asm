; this is an example of a simple hello world program!

; programs always start executing from the beginning of program memory
; therefore, the entry point is right here:
; use the echo op to print the immediate value
echo "hello world!"

; now loop saynig "hi" forevs
loop:
echo "hi"
jmp loop

halt 50%8
