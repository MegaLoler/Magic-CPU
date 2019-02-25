#!/usr/bin/env python3

import sys
from game import Game
from player import Player
from cpu import CPU

# this is a script in order to test out precompiled programs in a dummy game environment
# it's for demonstration and testing purposes

# usage: python run.py program.bin

# run a binary program stored in an external file as a player on some cpu
def run_file(filename, cpu, player):
    with open(filename, 'rb') as f:
        # load the program from the file
        program = f.read()
        # and tell the player to run that program
        return player.run_program(program, cpu)

# run a program stored in an extern file in a dummy game environment with a dummy player
def test_run(filename):
    # create the dummy game instance
    game = Game()
    # create the dummy player instance
    player = Player()
    # and create the CPU to run the program
    # cpu needs to know what game instance it belongs to in order to access the game's omni ram
    cpu = CPU(game)
    # and then run the program in the file
    return run_file(filename, cpu, player)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        # run the program and get the return value
        result = test_run(sys.argv[1])
        # print that return value
        print(f'The program completed: {result}')
    else: print(f'Usage: python {sys.argv[0]} program.bin')
