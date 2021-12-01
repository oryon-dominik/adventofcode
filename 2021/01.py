from puzzle_handler import AdventPuzzle
from log import log


"""These are dirty and hacky solutions but they work.. have to think it through more elegantly..."""


class SonarSweep(AdventPuzzle):
    approaches = {
            'previous': {"func": "compare_to_previous", "datatype": list},
            'window': {"func": "compare_window", "datatype": list},
        }
    puzzle_day = 1
    clean_data = True

    def clean(self, data):
        return [int(d) for d in data]

    def compare_to_previous(self):
        """How many measurements are larger than the previous measurement?"""
        increasing = 0
        for measurement, depth in enumerate(self.data):
            try:
                if self.data[measurement] > self.data[measurement - 1]:
                    log.debug(f"depth={depth} previous={self.data[measurement - 1]} increasing={depth - self.data[measurement - 1]}")
                    increasing += 1
            except IndexError:
                pass
        return increasing

    def compare_window(self, window_depth=3):
        """How many sums are larger than the previous sum?"""
        wd = window_depth
        increasing = 0
        for measurement, depth in enumerate(self.data):
            m = measurement
            n = m + 1
            try:
                this_ = sum(self.data[m : m + wd])
                next_ = sum(self.data[n: n + wd])
                log.debug(f"depth={depth} this_window={this_} next_window={next_} increasing={next_ - this_}")
                if this_ < next_:
                    increasing += 1
            except IndexError:
                pass
        return increasing


ssweep = SonarSweep(approach='previous', timeit=True)
log.info(f"{ssweep.text} | Task1 - Compare to previous: {ssweep.result} - {ssweep.time}")

ssweep = SonarSweep(approach='window', timeit=True)
log.info(f"{ssweep.text} | Task2 - Compare window: {ssweep.result} - {ssweep.time}")
