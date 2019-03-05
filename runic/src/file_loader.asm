; load the file to be compiled into ram
; load_file(filename)
load_file:
	; pop the filename 
	pull @r0%s

	; read in the data to the memory allocated to the source code
	echo "RIGHT NOW RIGHT NOW RIGHT NOW"
	read_file *source_code%s, @r0%s

	; return the read in string
	push @r0%s
	ret
