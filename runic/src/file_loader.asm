; load the file to be compiled into ram
; load_file(filename)
load_file:
	; pop the filename 
	pull @r0%s

	; read in the data
	read_file @source_code%s, @r0%s

	; done
	ret
