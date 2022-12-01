from handler import Puzzle
from logs import log


"""These are dirty and hacky solutions but they work.. have to think it through more elegantly..."""


class CalorieCountingAdvent(Puzzle):
    puzzle_day = 1
    clean_data = True

    def clean(self, data: str):
        return data.split('\n\n')

    def total_calories(self):
        return max([sum(int(e) for e in elf.split('\n')) for elf in self.data])

    def top_three_total_calories(self):
        return sum(sorted([sum(int(e) for e in elf.split('\n')) for elf in self.data])[-3:])


done = CalorieCountingAdvent(approach='total_calories', day=1, read_file_as='raw')
log.info(f"{done.text} | {done.approach.capitalize()}: {done.result} - {done.time}")

done = CalorieCountingAdvent(approach='top_three_total_calories', day=1, read_file_as='raw')
log.info(f"{done.text} | {done.approach.capitalize()}: {done.result} - {done.time}")
