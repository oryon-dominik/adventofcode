import itertools
import functools
import math
import time
from pathlib import Path


class ReportRepair:

    def __init__(
            self,
            subsequences_count: int,
            target: int = 2020,
            approach: str = 'itertools',  # does always work, slow
            timeit: bool = False,
        ):
        # the approaches we may use
        self.approaches = {
                'pythonic': {"func": self.pythonic_solution, "datatype": set},
                'itertools': {"func": self.linear_solution_itertools, "datatype": list},
                'binary': {"func": self.binary_solution, "datatype": list},
            }

        self.subsequences_count = subsequences_count
        self.target = target
        self.approach = approach
        self.timeit = timeit
        self.execution_time = None
        self.numbers = self.repair_data

    def read_data_from_file(self, file_path: str="01.data") -> list:
        """ read data from file and return lines as a list """
        path = Path(file_path)
        assert path.exists(), f"File {path.resolve()} not Found"
        with open(path.resolve(), "r") as file:
            data = [entry.replace("\n", "") for entry in file.readlines()]
        return data

    @property
    def repair_data(self):
        """repair the data we get from the file"""
        # we want to calculate with integers, so we convert the type
        data = [int(entry) for entry in self.read_data_from_file()]
        # converting the datatype to list or set, depending on the approach
        data = self.approaches.get(self.approach, {}).get("datatype", list)(data)
        # tests
        assert self.subsequences_count > 1, "Cannot compare less then two elements"
        assert type(data) == self.approaches.get(self.approach, {}).get("datatype", list)
        assert all([type(entry) == int for entry in data])
        return data

    @property
    def result(self) -> int:
        results = self.calc_results_from_approach(self.approach)
        # we should exactly have one result for these tasks
        assert len(results) == 1
        return results.pop()

    @property
    def time(self):
        if self.execution_time is None:
            return "Did not time the execution of the last method call"
        return f"Execution time: {self.execution_time :0.4f} seconds"

    def timer(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.execution_time = None
            if not self.timeit:
                return func(self, *args, **kwargs)
            time_start = time.perf_counter()
            value = func(self, *args, **kwargs)
            time_end = time.perf_counter()
            self.execution_time = time_end - time_start
            return value
        return wrapper

    def calc_results_from_approach(self, approach):
        assert approach in self.approaches, "approach not found"
        return self.approaches.get(approach, {}).get("func")()

    @timer
    def pythonic_solution(self) -> set:
        """to return one couple of a list we use a simple set"""
        assert self.subsequences_count <= 2, "This approach does not work for subsequences > 2"
        return {entry * complementary for entry in self.numbers if (complementary := self.target - entry) in self.numbers}

    @timer
    def linear_solution_itertools(self) -> list:
        """to return N combinations of a list of items we think of the itertools implementation"""
        # we put our results in that bucket
        results = []
        for combination in itertools.combinations(self.numbers, self.subsequences_count):
            # iterate through all possibilities and select..
            if sum(combination) == self.target:
                results.append(math.prod(combination))
        return results

    @timer
    def binary_solution(self) -> list:
        """to return N combinations of a list of items we think of
        a binary search implementation to speed up the search in lager datasets"""

        def binary_search_find_index(elements, value):
            left, right = 0, len(elements) - 1

            while left <= right:
                middle = (left + right) // 2

                if math.isclose(elements[middle], value):
                    return middle

                if elements[middle] < value:
                    left = middle + 1
                elif elements[middle] > value:
                    right = middle - 1
            return None

        def get_match_for_target(numbers, results, target):
            for number in numbers:
                target_value = target - number
                index = binary_search_find_index(numbers, target_value)
                if index is not None:
                    result = numbers[index]
                    # no doublettes
                    if number not in results:
                        results.append(number)
                    if result not in results:
                        results.append(result)
            return results

        def get_matches_for_targets(numbers, results, target):
            for number in numbers:
                intermediate_target = target - number
                results = get_match_for_target(numbers, results, intermediate_target)
            return results

        # binary search only works for a sorted array
        numbers = sorted(self.numbers)
        results = []
        target = self.target

        # this only works for 2 and 3 subsequences, TODO: enhance to recursively work with n
        if self.subsequences_count == 2:
            results = get_match_for_target(numbers, results, target)
        elif self.subsequences_count == 3:
            results = get_matches_for_targets(numbers, results, target)
        return [math.prod(results)]


# we will need the combinations of TWO subsequences for the first task
report = ReportRepair(subsequences_count=2, timeit=True)
print(f"Day 1, Task1 - LINEAR the expense report is: {report.result} - {report.time}")

# Task 2 wants us three combinations, so we just change the n
report = ReportRepair(subsequences_count=3, timeit=True)
print(f"Day 1, Task2 - LINEAR the expense report is: {report.result} - {report.time}")

# implemented some more approaches
report = ReportRepair(subsequences_count=2, timeit=True, approach="pythonic")
print(f"Day 1, Task1 - PYTHONIC the expense report is: {report.result} - {report.time}")
report = ReportRepair(subsequences_count=2, timeit=True, approach="binary")
print(f"Day 1, Task1 - BINARY the expense report is: {report.result} - {report.time}")
report = ReportRepair(subsequences_count=3, timeit=True, approach="binary")
print(f"Day 1, Task2 - BINARY the expense report is: {report.result} - {report.time}")
