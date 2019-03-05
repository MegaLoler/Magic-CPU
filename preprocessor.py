# this file is the preprocessor for the assembler
# preprocessor is used by including 'preprocessor directives' in your code
# these are lines that start with #, followed by the name of the directive, and maybe arguments
# basic use case example is to include other files into your code with '#include filename'

import os
import re

def include(directory, filename):
    ''' include another file into the code '''

    # get the file to include
    path = f'{directory}/{filename}'

    # replace the directive with the contents of this file
    with open(path, 'r') as f:
        contents = f.read()

    # recursively preprocess this as well!
    return preprocess(path, contents)

def preprocess(filename, code):
    ''' preprocess the code, taking care of any preprocessor directives '''

    # get the working directory of this file
    directory = os.path.dirname(filename)

    def repl(match):
        ''' function to replace directives '''
        directive = match.group(1)
        argument = match.group(2)

        if directive == 'include':
            return include(directory, argument)

        elif directive == 'nop':
            return ''

        else:
            raise Exception(f'Unknown preprocessor directive "{directive}"')

    # strip all comments as well
    # because the comments are being stripped here,
    # they could potentially be removed from the grammar
    # ACTUALLY.... causing problems INSIDE STRINGS soidk
    #code = re.sub(r'\;.*\n', '\n', code)

    # match directives (they are lines that start with #)
    code = re.sub(r'^\#(\w+)[ \t]*(.*)\n', repl, code, flags=re.MULTILINE)

    # return the postprocessed asssembly code
    return code
