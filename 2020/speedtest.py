from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class Speedtest(AdventPuzzleHandler):

    puzzle_day = 31
    clean_data = False
    approaches = {
        'speedtest': {"func": "run_long_calc", "datatype": list},
    }
    tries = 200_000_000

    def clean_data(self, data):
        return [d.split(';')[0] for d in data]

    def run_long_calc(self):
        cnt = 0
        for _ in range(self.tries):
            cnt += 1
        return cnt

speedtest = Speedtest(approach="speedtest", timeit=True)
speedtest.result
print(f"{speedtest.text} | Task1 - testing on: {speedtest.data[0]} - {speedtest.time}")

speedtest = Speedtest(approach="speedtest", timeit=True)
# print(f"{speedtest.text} | Task1 - testing on: {speedtest.data[1]} - {speedtest.time}")
