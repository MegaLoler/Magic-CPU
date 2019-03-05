;;; the toplevel compiler code

#include preprocessor.asm
#include lexer.asm
#include parser.asm
#include generator.asm

; compile runic code into runecore assembly
; return the compiled runecore
; compile(code)
compile:
	; preprocess
	; strips comments and deals with directives
	echo "Preprocessing..."
	call preprocess

	; tokenize the code
	echo "Tokenizing..."
	call lex

	; parse into an ast
	echo "Parsing..."
	call parse

	; generate code from the ast
	echo "Generating..."
	call generate

	; done
	ret
