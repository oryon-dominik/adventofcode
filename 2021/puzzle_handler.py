import functools
import time
import datetime
from pathlib import Path


class ReadFileAsPureFileMixin:
    def read_data_from_file(self, file_path) -> list:
        """Read data from file and return lines as a list."""
        path = Path(file_path)
        assert path.exists(), f"File {path.resolve()} not Found"
        with open(path.resolve(), "r") as file:
            data = file.read()
        return data


class AdventPuzzleHandler:
    puzzle_day = None
    approaches = None
    clean_data = None
    filename = None

    def __init__(self, approach: str, timeit: bool = False):
        # the approaches we may use
        self.approach = approach
        self.timeit = timeit
        self.execution_time = None
        self.get_approaches()
        self.data = self.repair_data()
        self.text = f"Advent of Code, Day {self.day}, {self.__class__.__name__}"

    @property
    def day(self):
        "Return the day of the puzzle."
        if not self.puzzle_day:
            raise NotImplementedError("You have to set the puzzle day as a class variable for the handler to work")
        return datetime.date(year=2020, month=12, day=self.puzzle_day).day

    def get_approaches(self):
        """
        Sum all aporaches.
        example:
            approaches = {
            'approach name': {"func": self.the_function_to_call, "datatype": list},
        }
        """
        def throw_no_approach():
            raise NotImplementedError("Implement valid approaches for the handler to work")
        if not self.approaches:
            throw_no_approach()
        self.processed_approaches = {}
        for approach, processing in self.approaches.items():
            function_name = processing.get("func")
            data_type = processing.get("datatype")
            if function_name is None or data_type is None:
                throw_no_approach()
            assert hasattr(self, function_name), f"Function for approach '{approach}' not found"
            func = getattr(self, function_name)
            self.processed_approaches.update({f"{approach}": {
                "func": func,
                "datatype": data_type,
            }})

    def read_data_from_file(self, file_path) -> list:
        """Read data from file and return lines as a list."""
        path = Path(file_path)
        assert path.exists(), f"File {path.resolve()} not Found"
        with open(path.resolve(), "r") as file:
            data = [entry.replace("\n", "") for entry in file.readlines()]
        return data

    def repair_data(self):
        """Repair the data we get from the file."""
        filename = self.filename if self.filename else f"{self.day:02d}.data"
        data = self.read_data_from_file(filename)
        # we convert the raw strings to the data we can handle
        # converting the datatype to list or set, depending on the approach
        data = self.approaches.get(self.approach, {}).get("datatype", list)(data)
        if self.clean_data is None:
            raise NotImplementedError("You should implement a method `clean_data` to clean your data, or set it to False")
        elif self.clean_data is False:
            cleaned_data = data
        else:
            cleaned_data = self.clean_data(data)

        # tests
        assert type(cleaned_data) == self.approaches.get(self.approach, {}).get("datatype", list)
        return cleaned_data

    @property
    def result(self):
        # we can directly return the result
        return self.calc_results_from_approach(self.approach)

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

    @timer
    def calc_results_from_approach(self, approach):
        assert approach in self.approaches, f"Not Found: {approach} is not a valid Approach"
        run = getattr(self, self.approaches.get(approach, {}).get("func"))
        return run()
