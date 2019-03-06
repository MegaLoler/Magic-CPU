;;; test some comparison ops

; 5 == 5
copy @0, 5
copy @1, 5
echo "a = "
echo @0
echo "b = "
echo @1
echo "a == b = "
eq @0, @1
echo @0
echo "-----------"

; 5 == 8
copy @0, 5
copy @1, 8
echo "a = "
echo @0
echo "b = "
echo @1
echo "a == b = "
eq @0, @1
echo @0
echo "-----------"

; 5 > 8
copy @0, 5
copy @1, 8
echo "a = "
echo @0
echo "b = "
echo @1
echo "a > b = "
gt @0, @1
echo @0
echo "-----------"

; 5 > 5
copy @0, 5
copy @1, 5
echo "a = "
echo @0
echo "b = "
echo @1
echo "a > b = "
gt @0, @1
echo @0
echo "-----------"

; 5 > 3
copy @0, 5
copy @1, 3
echo "a = "
echo @0
echo "b = "
echo @1
echo "a > b = "
gt @0, @1
echo @0
echo "-----------"

; 5 < 8
copy @0, 5
copy @1, 8
echo "a = "
echo @0
echo "b = "
echo @1
echo "a < b = "
lt @0, @1
echo @0
echo "-----------"

; 5 < 5
copy @0, 5
copy @1, 5
echo "a = "
echo @0
echo "b = "
echo @1
echo "a < b = "
lt @0, @1
echo @0
echo "-----------"

; 5 < 3
copy @0, 5
copy @1, 3
echo "a = "
echo @0
echo "b = "
echo @1
echo "a < b = "
lt @0, @1
echo @0
echo "-----------"

ret
