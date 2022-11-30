from handler import Puzzle
from logs import log


"""These are dirty and hacky solutions but they work.. have to think it through more elegantly..."""


class Advent(Puzzle):
    puzzle_day = 1

    def advent(self):
        data: list[int] = [int(d) for d in self.data]
        return sum(data)

done = Advent(approach='advent', day=1)
log.info(f"{done.text} | {done.approach.capitalize()}: {done.result} - {done.time}")
