# this file is the preprocessor for the assembler
# preprocessor is used by including 'preprocessor directives' in your code
# these are lines that start with #, followed by the name of the directive, and maybe arguments
# basic use case example is to include other files into your code with '#include filename'

import os
import re

def preprocess(filename, code):
    ''' preprocess the code, taking care of any preprocessor directives '''

    # get the working directory of this file
    directory = os.path.dirname(filename)

    def repl(match):
        ''' function to replace directives '''
        directive = match.group(1)
        argument = match.group(2)

        if directive == 'include':

            # get the file to include
            path = f'{directory}/{argument}'

            # replace the directive with the contents of this file
            with open(path, 'r') as f:
                contents = f.read()

            # recursively preprocess this as well!
            processed = preprocess(path, contents)

            # and return the results as the replacement
            return f'{processed}\n'

        elif directive == 'nop':
            return '\n'

        else:
            raise Exception(f'Unknown preprocessor directive "{directive}"')

    # match directives (they are lines that start with #)
    # TODO: find a better regexp that matches directives at the beginning of the file as well
    code = re.sub(r'\n\#(\w+)[ \t]*(.*)\n', repl, code)

    # return the postprocessed asssembly code
    return code
