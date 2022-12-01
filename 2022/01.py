from handler import Puzzle, approach


class CalorieCounting(Puzzle):
    clean_data = True

    def clean(self, data: str):
        return data.split('\n\n')

    @approach
    def total_calories(self):
        return max([sum(int(e) for e in elf.split('\n')) for elf in self.data])

    @approach
    def top_three_total_calories(self):
        return sum(sorted([sum(int(e) for e in elf.split('\n')) for elf in self.data])[-3:])


CalorieCounting(day=1, read='raw').info()

