;;; memory management stuff

; where the pointer to the top of dynamically allocated memory is
mem_pointer=200h

; where the mem pointer is initialized to
mem_base=202h

; setup dynamic memory
init_mem:
	copy @mem_pointer%16, mem_base
	ret

; allocate some memory
; alloc(bytes)
; return pointer and how much was allocated
alloc:
	; grab the requested size
	; r0 = byte count
	pull @r0%16

	; save the current pointer
	; it will be the pointer to the new data
	copy @r2%16, @mem_pointer%16

	; increment the pointer
	add @mem_pointer%16, @r0%16

	; return pointer and size
	push @r0%16	; byte count
	push @r2%16	; pointer
	ret
