#!/usr/bin/env python3

import sys
import operation # importing to prevent weird import order issues?
from game import Game
from player import Player
from cpu import CPU
from memory import FileMemory

# this is a script in order to test out precompiled programs in a dummy game environment
# it's for demonstration and testing purposes

# usage: python run.py program.bin

def run_file(filename, cpu, player, game):
    ''' run a binary program stored in an external file as a player on some cpu '''

    # load the program memory from the file
    program_memory = FileMemory(filename)

    # and make the player run it
    return player.run_program(program_memory, cpu, game)

def test_run(filename):
    ''' run a program stored in an extern file in a dummy game environment with a dummy player '''

    # create the dummy game instance
    game = Game()

    # create the dummy player instance
    player = Player()

    # and create the CPU to run the program
    cpu = CPU()

    # and then run the program in the file
    return run_file(filename, cpu, player, game)

if __name__ == '__main__':
    if len(sys.argv) == 2:

        # run the program and get the return value
        result = test_run(sys.argv[1])

        # print that return value
        print(f'The program completed: {result}')
        
    else: print(f'Usage: python {sys.argv[0]} program.bin')
