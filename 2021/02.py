from puzzle_handler import AdventPuzzle
from log import log
from typing import NamedTuple
from rich import print


class Instruction(NamedTuple):
    opcode: str
    x: int


class Dive(AdventPuzzle):
    approaches = {
            'position': {"func": "calculate_position"},
            'aim': {"func": "calculate_position_with_aim"},
        }
    puzzle_day = 2
    clean_data = True

    def clean(self, data):
        data = [entry.split(' ') for entry in data]
        return [Instruction(opcode=d[0], x=int(d[1])) for d in data]

    def calculate_position(self, horizontal_position = 0, depth = 0):
        """
        What do you get if you multiply your final horizontal position
        by your final depth
        """
        for instruction in self.data:
            match instruction.opcode:
                case "forward":
                    horizontal_position += instruction.x
                case "down":
                    depth += instruction.x
                case "up":
                    depth -= instruction.x
        return horizontal_position * depth

    def calculate_position_with_aim(self, horizontal_position = 0, depth = 0, aim = 0):
        """
        What do you get if you multiply your final horizontal position
        by your final depth - using the "aim approach".
        """
        for instruction in self.data:
            match instruction.opcode:
                case "forward":
                    horizontal_position += instruction.x
                    depth += aim * instruction.x
                case "down":
                    aim += instruction.x
                case "up":
                    aim -= instruction.x
        return horizontal_position * depth


dive = Dive(approach='position', timeit=True)
log.info(f"{dive.text} | Task1 - Calculate position mulitplier: {dive.result} - {dive.time}")

dive = Dive(approach='aim', timeit=True)
log.info(f"{dive.text} | Task2 - Compare poistion with aim: {dive.result} - {dive.time}")
