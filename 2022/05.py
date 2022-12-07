from typing import Any, NamedTuple
from copy import deepcopy

import parse
import more_itertools as mit

from handler import Puzzle, approach



class Move(NamedTuple):
    weight: int  # how many crates to move
    source: int  # from which stack
    destination: int  # to which stack


class CrateStack(NamedTuple):
    index: int
    crates: list[str]


class Ship(NamedTuple):
    stacks: list[CrateStack]
    moves: list[Move]



class SupplyStacks(Puzzle):
    clean_data = True


    def read_stacks(self, raw_stacks: str) -> list:
        stacks: list = raw_stacks.split('\n')
        numbers = [int(n.strip()) for n in stacks.pop().split(' ') if n.strip() != '']
        crate_stacks = [CrateStack(index=n, crates=[]) for n in range(1, len(numbers) + 1)]
        for stack in reversed(stacks):
            # supported since python >= 3.12 -> itertools.batched(stack, 4)
            for index, crate in enumerate(mit.chunked(stack, 4)):
                pick = crate[1]
                if pick != ' ':
                    [s for s in crate_stacks if s.index == index + 1][0].crates.append(pick)
        return crate_stacks

    def clean(self, data: str) -> Ship:
        parser = parse.compile("move {} from {} to {}")
        stacks, moves = data.split('\n\n')
        moves = [Move(*(map(int, parser.parse(m).fixed))) for m in moves.split('\n')]  # type: ignore
        return Ship(stacks=self.read_stacks(stacks), moves=moves)

    @approach
    def what_crate_is_on_top_of_each_stack_crate_mover_9000(self) -> str:
        self.data: Ship
        ship = deepcopy(self.data)
        for move in ship.moves:
            for _ in range(move.weight):  # move the crane move.weight times
                source = [s for s in ship.stacks if s.index == move.source][0]
                destination = [s for s in ship.stacks if s.index == move.destination][0]
                moving = source.crates.pop()
                destination.crates.append(moving)

        return ''.join([s.crates[-1] for s in ship.stacks])

    @approach
    def what_crate_is_on_top_of_each_stack_crate_mover_9001(self) -> str:
        self.data: Ship
        ship = deepcopy(self.data)
        for move in ship.moves:
            # the crane moves all move.weight items at once
            source = [s for s in ship.stacks if s.index == move.source][0]
            destination = [s for s in ship.stacks if s.index == move.destination][0]

            moving = source.crates[-move.weight:]  # pickup
            for _ in range(len(moving)):
                source.crates.pop()

            for m in moving:
                destination.crates.append(m)  # drop

        return ''.join([s.crates[-1] for s in ship.stacks])



if __name__ == '__main__':
    advent = SupplyStacks(day=5, read='raw')
    advent.info()
