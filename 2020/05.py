import math
import numpy as np
from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class BinaryBoarding(AdventPuzzleHandler):

    puzzle_day = 5
    clean_data = False
    approaches = {
        'prepare aircraft': {"func": "seat_passengers", "datatype": list},
        'find seat id': {"func": "get_your_seat_id", "datatype": list},
    }
    rows_in_the_plane = range(2**7)
    seats_in_a_row = range(2**3)
    seats_in_the_plane = len(rows_in_the_plane) * len(seats_in_a_row)

    def __init__(self, approach: str, timeit: bool):
        super().__init__(approach, timeit=timeit)
        self.airplane = np.full(
        shape=(len(self.rows_in_the_plane), len(self.seats_in_a_row)),
        fill_value=np.nan,
        dtype=np.float64,
    )

    def binary_find_seat(self, boarding_pass_instructions):
        instructions = boarding_pass_instructions
        instructions = instructions.replace("F", "0")
        instructions = instructions.replace("B", "1")
        instructions = instructions.replace("L", "0")
        instructions = instructions.replace("R", "1")
        calculus = int(instructions, 2)
        return calculus

    def get_your_seat_id(self):
        error = "The Aircraft should be empty at start"
        assert np.count_nonzero(np.isnan(self.airplane)) == self.seats_in_the_plane, error
        self.seat_passengers()
        free_seats = np.count_nonzero(np.isnan(self.airplane))
        print(f'>>> DEBUG: {free_seats}')
        # TODO: remove the first and last rows

    def seat_passengers(self):
        seat_ids = []
        for seat in self.data:
            boarding_pass_row = seat[:7]
            row_of_this_seat = self.binary_find_seat(boarding_pass_row)
            boarding_pass_col = seat[7:]
            seat_in_the_row = self.binary_find_seat(boarding_pass_col)
            seat_id = row_of_this_seat * 8 + seat_in_the_row
            seat_ids.append(seat_id)
            self.airplane[row_of_this_seat, seat_in_the_row] = seat_id
        return max(seat_ids)

boarding = BinaryBoarding(approach="prepare aircraft", timeit=True)
print(f"{boarding.text} | Task1 - find your seat: {boarding.result} - {boarding.time}")

boarding = BinaryBoarding(approach="find seat id", timeit=True)
print(f"{boarding.text} | Task2 - find your seat: {boarding.result} - {boarding.time}")
