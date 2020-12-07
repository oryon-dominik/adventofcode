

opcodes = {
    9: {
        "name": "relative base offset",
        "instruction": "add to relative_base",
        "param_lenght": 1,
        "description": "adjusts relative base"
    }
}

def intcode_computer(memory_array, extended_memory=None, mode=2):  # mode 2 = relative mode
    relative_base = 0
    # TODO: support large numbers
    if extended_memory is None:
        extended_memory = []
    referring_address = self_address + relative_base


def basic_operation_of_system_test(mode):  # BOOST
    if mode == 1:
        print('activate testmode')
    # check every opcode output any opcodes (and the associated parameter
    # modes) that seems to be functioning incorrectly -> output BOOST keycode
    
    # Once your Intcode computer is fully functional, the BOOST program should
    # report no malfunctioning opcodes when run in test mode; it should only
    # output a single value, the BOOST keycode.


# TESTS
test_input = 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
# should output a Quine [https://en.wikipedia.org/wiki/Quine_(computing)]
assert intcode_computer(test_input) == test_input
test_input = 1102,34915192,34915192,7,4,7,99,0
assert len(intcode_computer(test_input)) == 16
test_input = 104,1125899906842624,99
assert intcode_computer(test_input) == 1125899906842624

