;;; indirect addressing mode tests

var=50

copy @0%16, var

copy @@0, 5
echo @@0
dump

ret
