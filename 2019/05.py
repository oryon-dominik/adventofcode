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
opcode 3
    take input and store at position of only parameter
opcode 4
    output the value at address of parameter
"""

parameter_modes = {
    0: "position_mode",  # returns value of position on memory[parameter]
    1: "immediate_mode",  # returns value of parameter
}

instruction_codes = [
    "the last two digits are opcode",
    "the digits before that are the parameter_modes (from last to first) for the single parameters provided",
    "missing modes are 0",  # even if leading
    ]

# Parameters that an instruction writes to will never be in immediate mode



def read_opcodes_from_file(file_="05.data"):
    """ read the operation codes for your spaceship """
    with open(file_, "r") as operations_file:
        operations = operations_file.readlines()
        operations = [int(o) for o in operations[0].split(',')]
    return operations


def handle_opcodes(memory: list) -> list:
    for postion in memory:
        pass
        # move instruction pointer += number of values in instruction

def thermal_environment_supervision_terminal(test_id=1):  # TEST
    """ runs series of diagnostic tests
    
    test_ids:
        1: ship's air conditioner unit
    """
    # test_id = input("ID of system to TEST")
    diagnostic_program = read_opcodes_from_file()
    bias = expected_output - output
    if test_id:
        return 0 # if test was successful
    return bias  # not working correctly

    # finally: return diagnostic_code, HALT_PROGRAM


# old TESTS
operations = [1,0,0,0,99]
assert handle_opcodes(operations) == [2,0,0,0,99]
operations = [2,3,0,3,99]
assert handle_opcodes(operations) == [2,3,0,6,99]
operations = [2,4,4,5,99,0]
assert handle_opcodes(operations) == [2,4,4,5,99,9801]
operations = [1,1,1,4,99,5,6,0,99]
assert handle_opcodes(operations) == [30,1,1,4,2,5,6,0,99]

# start program
operations = read_opcodes_from_file()


# # "1202 program alarm" state
# program = operations.copy()
# noun, verb = 12, 2
# program, result = run(program, noun, verb)


# Task2, maybe should have rearranged our handle program to listen to an
# instruction_pointer with opcode & parameters
# where instruction_pointer += count(opcode + parameters)
# because we may be ignoring that 99 only has a lenght of 1 STEP now
# (not 4 STEPS, as we pretend in our function) this is not important for now,
# because 99 quits the program. It could be very relevant when we have uneven
# instruction lenght otherwise though..

test = "test"
print(f"Day 5, Task 1 - The result is: {test}")

