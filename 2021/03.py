from typing import List
from puzzle_handler import AdventPuzzle
from log import log


class MissingBinaryPosition(Exception):
    pass

class BinaryDiagnostic(AdventPuzzle):
    approaches = {
            'power': {"func": "power_consumption",},
            'life': {"func": "life_supporting_rate",},
        }
    puzzle_day = 3

    def power_consumption(self) -> int:
        """
        What is the power consumption of the submarine?

        gamma-rate: the most common bit for bit in bits [positon-wise] (vertical [column] analysis)
        epsilon-rate: the inverse of gamma (it's actually the least common bit for bit in bits...)
        """
        gamma = self.calculate_gamma()
        epsilon = self.calculate_epsilon_from_gamma(gamma=gamma)
        return self.binary_string_to_int(gamma) * self.binary_string_to_int(epsilon)

    def life_supporting_rate(self):
        """
        What is the life support rating of the submarine?
        """
        # oxygen generator rating 
        oxygen = self.calculate_oxygen_generator_rating()
        # CO2 scrubber rating
        co2 = self.calculate_co2_scrubber_rating()
        return self.binary_string_to_int(oxygen) * self.binary_string_to_int(co2)

    def calculate_oxygen_generator_rating(self):
        data = self.data
        for column in range(self.get_minimum_data_length()):
            most_common_bit = self.get_most_common_bit(transposed_data=self.transpose_list(data), column=column, reverse=True)
            data = self.filter_list_for_bits(data, bit=most_common_bit, column=column)
        assert len(data) == 1, f"There should only be one row left. Got: {data}"
        return data[0]

    def calculate_co2_scrubber_rating(self):
        data = self.data
        for column in range(self.get_minimum_data_length()):
            least_common_bit = self.get_least_common_bit(transposed_data=self.transpose_list(data), column=column, reverse=False)
            data = self.filter_list_for_bits(data, bit=least_common_bit, column=column)
        assert len(data) == 1, f"There should only be one row left. Got: {data}"
        return data[0]

    def calculate_gamma(self) -> str:
        return ''.join(
            [
                self.get_most_common_bit(self.transpose_list(self.data), column=column)
                for column in range(self.get_minimum_data_length())
            ]
        )

    def calculate_epsilon_from_gamma(self, gamma: str) -> str:
        """Epsilon is 'just' the inverse of gamma."""
        return self.inverse_binary_string(binary_string=gamma)

    def filter_list_for_bits(self, data: List[str], bit: str, column: int):
        """
        Filter the data by removing all rows that don't have the bit in the column.
        """
        return [row for row in data if bit in row[column]]

    def get_minimum_data_length(self, data=None):
        """Get the minimal length of the rows."""
        if data is None:
            data = self.data
        lengths = [len(d) for d in data]
        return min(lengths)

    def inverse_binary_string(self, binary_string: str):
        return ''.join(['1' if i == '0' else '0' for i in binary_string])

    def binary_string_to_int(self, binary_string: str):
        return int(binary_string, 2)

    def transpose_list(self, list_of_lists: List[str] | List[list]):
        return list(map(list, zip(*list_of_lists)))

    def get_most_common_bit(self, transposed_data: list, column: int, reverse=True):
        """
        If there is a tie, '1' is returned.
        You can reverse this behaviour and return '0' on a tie by setting reverse to False.
        """
        bits = transposed_data[column]
        most_common_bit = max(sorted(bits, reverse=reverse), key=bits.count)
        return most_common_bit

    def get_least_common_bit(self, transposed_data: list, column: int, reverse=False):
        """
        If there is a tie, '0' is returned.
        You can reverse this behaviour and return '1' on a tie by setting reverse to True.
        """
        bits = transposed_data[column]
        least_common_bit = min(sorted(bits, reverse=reverse), key=bits.count)
        return least_common_bit

    def tests(self, results):
        """Run the tests for the puzzle."""
        log.debug(f"Running tests for puzzle day {self.puzzle_day}")
        # Part 1
        data = [
            "00100",
            "11110",
            "10110",
            "10111",
            "10101",
            "01111",
            "00111",
            "11100",
            "10000",
            "11001",
            "00010",
            "01010",
        ]
        gamma = ""
        for column in range(self.get_minimum_data_length(data=data)):
            common_bit = self.get_most_common_bit(self.transpose_list(data), column=column)
            gamma += common_bit
        assert gamma == "10110"
        assert type(results) is int, "Results should be an integer"

        # test lists are transposable
        original_list = ['0', '1']
        transposed = self.transpose_list(original_list)
        assert transposed == [['0', '1']]
        # tests that assure ties are handled correctly
        # most common bit
        most_common = self.get_most_common_bit(transposed_data=transposed, column=0)
        assert most_common == "1", f"Most common should be 1. Is {most_common}"
        most_common = self.get_most_common_bit(transposed_data=transposed, column=0, reverse=True)
        assert most_common == "1", f"Most common should be 1. Is {most_common}"
        most_common = self.get_most_common_bit(transposed_data=transposed, column=0, reverse=False)
        assert most_common == "0", f"Most common should be 0. Is {most_common}"
        # least common bit
        least_common = self.get_least_common_bit(transposed_data=transposed, column=0)
        assert least_common == "0", f"Least common should be 0. Is {least_common}"
        least_common = self.get_least_common_bit(transposed_data=transposed, column=0, reverse=False)
        assert least_common == "0", f"Least common should be 0. Is {least_common}"
        least_common = self.get_least_common_bit(transposed_data=transposed, column=0, reverse=True)
        assert least_common == "1", f"Least common should be 1. Is {least_common}"


binarydiagnostic = BinaryDiagnostic(approach='power', timeit=True)
log.info(f"{binarydiagnostic.text} | Task1 - Calculate power consumption: {binarydiagnostic.result} - {binarydiagnostic.time}")

binarydiagnostic = BinaryDiagnostic(approach='life', timeit=True)
log.info(f"{binarydiagnostic.text} | Task2 - Calculate life supporting rate: {binarydiagnostic.result} - {binarydiagnostic.time}")
