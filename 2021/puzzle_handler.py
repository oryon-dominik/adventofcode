import functools
import time
import datetime
from pathlib import Path
from typing import Union
from log import log


class FileRaw:
    def read_data_from_file(self, path: Path) -> str:
        """Read data from file and return lines as a list."""
        with open(path.resolve(), "r") as file:
            data = file.read()
        return data

class FileAsList:
    def read_data_from_file(self, path: Path) -> list:
        """Read data from file and return lines as a list."""
        with open(path.resolve(), "r") as file:
            data = [entry.replace("\n", "") for entry in file.readlines()]
        return data


class AdventPuzzle:
    puzzle_day = None
    approaches = None
    clean_data = False
    convert_datatype = False
    filen_ame = None
    enforce_tests = False

    def __init__(self, approach: str, timeit: bool = False, file_handler: Union[FileRaw, FileAsList] = FileAsList()):
        # the approaches we may use
        self.approach = approach
        self.timeit = timeit
        self.file_handler = file_handler
        self.execution_time = None
        self._init_approaches()
        self.data = self._read_convert_and_clean_data()
        self.text = f"Advent of Code, Day {self.day}, {self.__class__.__name__}"

    @property
    def day(self):
        "Return the day of the puzzle."
        if not self.puzzle_day:
            raise NotImplementedError("You have to set the puzzle day as a class variable for the handler to work")
        return datetime.date(year=2020, month=12, day=self.puzzle_day).day

    def _init_approaches(self) -> dict:
        """
        Build a dict with all approaches.

        returns (example):
            approaches = {
                'approach name': {"func": self.the_function_to_call, "datatype": list},
            }
        """

        def throw_no_approach():
            raise NotImplementedError("Implement valid approaches for the handler to work: approaches = {'approach name': {'func': 'functionname', Optional['datatype': list|set]} }")

        if self.approaches is None:
            throw_no_approach()

        self.processed_approaches = {}
        for approach, processing in self.approaches.items():
            # get the function to call, and the datatype to return
            function_name = processing.get("func")
            data_type = processing.get("datatype")
            if function_name is None:
                throw_no_approach()
            if data_type is None and self.convert_datatype:
                throw_no_approach()
            assert hasattr(self, function_name), f"Function for approach '{approach}' not found."
            if self.convert_datatype:
                assert data_type in [list, set], f"Datatype for approach '{approach}' not valid. Use list or set."
            func = getattr(self, function_name)
            self.processed_approaches.update({f"{approach}": {
                "func": func,
                "datatype": data_type,
            }})
        return self.processed_approaches

    def _path_from_filename(self, filename: str) -> Path:
        """Return the path to the file."""
        path = Path(filename)
        if not any([c in filename for c in ('/', '\\')]):
            parent = Path(__file__).parent
            path = parent / filename
        assert path.exists(), f"File {path.resolve()} not Found"
        return path

    def _read_data_from_file(self, path: Path) -> list:
        """Read data from file."""
        if not self.file_handler or not hasattr(self.file_handler, "read_data_from_file"):
            raise NotImplementedError(f"You should implement your own data-processing-method 'read_data_from_file' in the handler {self.file_handler.__name__}.")
        return self.file_handler.read_data_from_file(path=path)

    def clean(self, data):
        raise NotImplementedError("You should implement a method `clean(self, data)` to clean your data, or set the 'clean_data' property to False.")

    def _read_convert_and_clean_data(self) -> Union[list, set]:
        """Read the data and convert it to the expected data_type (list or set)."""
        filename = self.filename if self.filename is not None else f"{self.day:02d}.data"
        data = self._read_data_from_file(path=self._path_from_filename(filename=filename))
        # we convert the raw strings to the data we can handle
        # converting the datatype to list or set, depending on the approach
        if self.convert_datatype:
            data = self.approaches.get(self.approach, {}).get("datatype", list)(data)
        if self.clean_data:
            data = self.clean(data)
        return self.test_data(data)

    def test_data(self, cleaned_data):
        """Test the result of the function."""
        if self.convert_datatype:
            assert type(cleaned_data) == self.approaches.get(self.approach, {})["datatype"], f"Datatype of the result is not the expected one. Expected: {self.approaches.get(self.approach, {})['datatype']}, got: {type(cleaned_data)}."
        return cleaned_data

    def tests(self, results):
        """Run the tests for the puzzle."""
        # -> assert some conditions that should be met.
        if self.enforce_tests:
            raise NotImplementedError("You should implement a method `tests(self, results)` to run the tests for the puzzle if 'enforce_tests' is True.")
        return True

    def run_tests(self, results, error = None):
        """Run the tests for the puzzle."""
        passed = False
        try:
            passed = self.tests(results=results)
        except AssertionError as e:
            error = e
        if not passed:
            log.error(f"Tests for puzzle {self.text} failed: {error}")
        return results

    @property
    def result(self):
        """
        Used as a convenience property for neater access.
        Usally, we can directly return the result.
        """
        return self.run_tests(self._calc_results_from_approach(self.approach))

    @property
    def time(self) -> str:
        """Return a str of the execution time of the last run."""
        if self.execution_time is None:
            return "Did not time the execution of the last method call."
        return f"Execution time: {self.execution_time :0.4f} seconds."

    def timer(func):
        """Decorator to time the execution of a function."""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.execution_time = None
            if not self.timeit:
                # Don't time the execution, just return the result
                return func(self, *args, **kwargs)
            # Time it. Execute. Return.
            time_start = time.perf_counter()
            value = func(self, *args, **kwargs)
            time_end = time.perf_counter()
            self.execution_time = time_end - time_start
            return value
        return wrapper

    @timer
    def _calc_results_from_approach(self, approach):
        """Unpack the function from apporaches und call it."""
        assert approach in self.approaches, f"Not Found: {approach} is not a valid Approach."
        run = getattr(self, self.approaches.get(approach, {}).get("func"))
        return run()
