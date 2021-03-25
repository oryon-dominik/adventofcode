from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class MatchSticks(ReadFileAsPureFileMixin, AdventPuzzleHandler):

    puzzle_day = 8
    approaches = {
        'eval': {"func": "eval_me", "datatype": list},
    }

    def clean_data(self, data):
        return "".join(data).split('\n')


    def eval_me(self):
        in_memory = sum([len(d) for d in self.data])
        literals = sum([len(eval(d)) for d in self.data])
        return in_memory - literals


sticks = MatchSticks(approach="eval", timeit=True)
print(f"{sticks.text} | Task1 - sticks: {sticks.result} - {sticks.time}")

# Advent of Code, Day 8, MatchSticks | Task1 - sticks: 1333 - Execution time: 0.0014 seconds
