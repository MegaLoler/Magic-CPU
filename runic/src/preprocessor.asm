;;; the runic preprocessor

; strips comments, and deals with directives
; preparing the code for the parser
; preprocess(code)
preprocess:
	;; first strip comments

	; r0 = code
	pull @r0%s	
	repl @r0%s, "//.*\n", ""
	push @r0%s	

	;; now process directives (macros, etc)
	; TODO

	; done
	ret
