import string
import itertools

import more_itertools as mit

from handler import Puzzle, approach


class CampCleanup(Puzzle):

    def tests(self, results):
        assert self.get_range([1, 1]) == [1], "Zero range should contain one element"
        assert self.get_range([0, 2]) == [0, 1, 2], "Range shall be inclusive."

    def get_range(self, sections: list):
        if sections[0] == sections[-1]:
            return [sections[0]]
        return list(range(sections[0], sections[-1] + 1))

    @approach
    def count_assignment_pairs(self) -> int:
        overlapping = 0
        cleaning_elves = ((list(map(int, elf.split('-'))) for elf in elves.split(',')) for elves in self.data)
        for cleaned_section_ids_1, cleaned_section_ids_2 in cleaning_elves:
            first, second = self.get_range(cleaned_section_ids_1), self.get_range(cleaned_section_ids_2)
            the_pairs_overlap: bool = len(set(first) & set(second)) > 0
            if the_pairs_overlap:
                overlapping += 1
        return overlapping

    @approach
    def find_double_cleaners(self) -> int:
        ranges = []
        cleaning_elves = ((list(map(int, elf.split('-'))) for elf in elves.split(',')) for elves in self.data)
        for cleaned_section_ids_1, cleaned_section_ids_2 in cleaning_elves:
            first, second = self.get_range(cleaned_section_ids_1), self.get_range(cleaned_section_ids_2)
            if all(section in second for section in first) or all(section in first for section in second):
                # Rebuild the initial string, for its beauty 👾
                ranges.append(",".join([
                    "-".join([str(i) for i in [list(cleaned_section_ids_1)[0], list(cleaned_section_ids_1)[-1]]]),
                    "-".join([str(i) for i in [list(cleaned_section_ids_2)[0], list(cleaned_section_ids_2)[-1]]])
                ]))
        return len(ranges)


if __name__ == '__main__':
    advent = CampCleanup(day=4)
    advent.info()
