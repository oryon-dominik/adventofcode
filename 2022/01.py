from handler import Puzzle
from logs import log


"""These are dirty and hacky solutions but they work.. have to think it through more elegantly..."""


class DayOne(Puzzle):
    puzzle_day = 1

    def advent(self):
        data: list[int] = [int(d) for d in self.data]
        return sum(data)

done = DayOne(approach='advent', timeit=True, day=1, read_file_as='lines')
log.info(f"{done.text} | {done.approach.capitalize()}: {done.result} - {done.time}")
