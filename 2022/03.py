import string
import itertools

import more_itertools as mit

from handler import Puzzle, approach


class RucksackReorganization(Puzzle):

    def priorities(self) -> dict:
        alphabet = string.ascii_lowercase + string.ascii_uppercase
        priorities = range(1, len(alphabet) + 1)
        return {char: priority for char, priority in zip(alphabet, priorities)}

    @approach
    def get_priorities_straight(self):
        summed_up = 0
        for elvenrucksack in self.data:
            packed = len(elvenrucksack)
            first, second = elvenrucksack[:packed // 2], elvenrucksack[packed // 2:]
            summed_up += self.priorities()[''.join(set(first) & set(second))]
        return summed_up

    @approach
    def authorized_elves(self, batch_size: int=3):
        # FIXME: batched = itertools.batched(self.data, batch_size)  # supported since python >= 3.12
        batched = mit.chunked(self.data, batch_size)
        summed_up = 0
        for elves in batched:
            first, second, third = elves  # rucksacks
            badge = set(first) & set(second) & set(third)
            summed_up += self.priorities()[''.join(badge)]
        return summed_up


if __name__ == '__main__':
    advent = RucksackReorganization(day=3)
    advent.info()
