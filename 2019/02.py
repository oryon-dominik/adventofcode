#!/usr/bin/env python3
# coding: utf-8

"""
Santas spaceship (Intcode computer)
has a 1202 Program Alarm

opcode 99:
    finishes program
    
opcode 1:
    take value at position 1
    take Value at position 2
    add them and store at position 3
opcode 2:
    same as opcode 2 but with mulitplying instad of adding
"""

import random


STEPS = 4


def read_opcodes_from_file(file_="02.data"):
    """ read the operation codes for your spaceship """
    with open(file_, "r") as operations_file:
        operations = operations_file.readlines()
        operations = [int(o) for o in operations[0].split(',')]
    return operations


def handle(ops: list) -> list:
    for position in range(0, len(ops), STEPS):
        opcode = ops[position]
        if opcode == 99:
            return ops
        elif opcode == 1:
            ops[ops[position + 3]] = ops[ops[position + 1]] + ops[ops[position + 2]]
        elif opcode == 2:
            ops[ops[position + 3]] = ops[ops[position + 1]] * ops[ops[position + 2]]


def run(operations, noun, verb):
    operations[1] = noun
    operations[2] = verb
    # restoring the gravity assist program
    operations = handle(operations)
    result = operations[0]
    return operations, result


# TESTS
operations = [1,0,0,0,99]
assert handle(operations) == [2,0,0,0,99]
operations = [2,3,0,3,99]
assert handle(operations) == [2,3,0,6,99]
operations = [2,4,4,5,99,0]
assert handle(operations) == [2,4,4,5,99,9801]
operations = [1,1,1,4,99,5,6,0,99]
assert handle(operations) == [30,1,1,4,2,5,6,0,99]


# start program
operations = read_opcodes_from_file()


# "1202 program alarm" state
program = operations.copy()
noun, verb = 12, 2
program, result = run(program, noun, verb)

print(f"Day 2, Task1 the operation at position 0 is: {program[0]}")


def generate_output_from(operations, output=19690720):
    result = None
    counter = 0
    while result != output:
        counter += 1
        print('\r>>> Round:', f'{counter}', end="")
        ops = operations.copy()
        # HACK: randomly picking the values until we match is fast enough for now
        noun = random.randint(0, 100)
        verb = random.randint(0, 100)
        # better:
        #    from itertools import product
        #    for noun, verb in product(range(100), repeat=2):
        ops, result = run(ops, noun, verb)
    print(f"\r>>> Round: {counter} FINISHED")
    return noun, verb

# Task2, maybe should have rearranged our handle program to listen to an
# instruction_pointer with opcode & parameters
# where instruction_pointer += count(opcode + parameters)
# because we may be ignoring that 99 only has a lenght of 1 STEP now
# (not 4 STEPS, as we pretend in our function) this is not important for now,
# because 99 quits the program. It could be very relevant when we have uneven
# instruction lenght otherwise though..

output = 19690720
noun, verb = generate_output_from(operations, output)

print(f"Day 2, Task2 the answer 100* (noun={noun}) + (verb={verb}) where result is {output} is: {100 * noun + verb}")
