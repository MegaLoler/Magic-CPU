; load the file to be compiled into ram
; load_file(filename)
load_file:
	; pop the filename 
	pull @r0%s

	; read in the data
	read_file @r0%s, @r0%s

	; return the read in string
	push @r0%s
	ret
