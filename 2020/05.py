from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class BinaryBoarding(AdventPuzzleHandler):

    puzzle_day = 5
    clean_data = False
    approaches = {
        'find seat': {"func": "seat_passengers", "datatype": list},
    }

    def seat_passengers(self):
        return


boarding = BinaryBoarding(approach="find seat", timeit=True)
print(f"{boarding.text} | Task1 - find your seat: {boarding.result} - {boarding.time}")

boarding = BinaryBoarding(approach="find seat", timeit=True)
print(f"{boarding.text} | Task2 - find your seat: {boarding.result} - {boarding.time}")
