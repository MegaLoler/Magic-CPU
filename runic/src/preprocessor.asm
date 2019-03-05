;;; the runic preprocessor

; strips comments, and deals with directives
; preparing the code for the parser
; preprocess(code)
preprocess:
	;; first strip comments
	repl @@source_code%s, "//.*\n", ""

	;; now process directives (macros, etc)
	; TODO

	; done
	ret
