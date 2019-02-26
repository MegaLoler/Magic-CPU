;;; fizz buzz example

; start at 1
copy @0, 1

;; start of the fizz buzz loop
loop:

; see if fizz
copy @1, @0
; divis by 3?
mod @1, 3

; see if buzz
copy @2, @0
; divis by 5?
mod @2, 5

; sse if fizzbuzz
; (that means if both fizz and buzz lol)
copy @3, @1
bor @3, @2

; say fizzbuzz if fizzbuzz
; so skip if not
jmpif @3, skip1
echo "fizzbuzz"
jmp done
skip1:

; say fizz if fizz
jmpif @1, skip2
echo "fizz"
jmp done
skip2:

; say buzz if buzz
jmpif @2, skip3
echo "buzz"
jmp done
skip3:

; otherwise just say the dang numeral lol
echo @0
done:

;; increment and stop at 100
inc @0
; copy the current counter value
copy @1, @0
; subtract 100
sub @1, 100
; if the result is 0, we reached 100
; otherwise, loop
jmpif @1, loop

; done
halt 0
