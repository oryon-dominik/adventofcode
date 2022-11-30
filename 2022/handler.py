import functools
import time
import datetime
import types
from pathlib import Path

from typing import Literal, Any, Callable
from logs import log
from inout import read


YEAR = 2022


class Puzzle:
    approaches = None
    clean_data = False
    filename = None
    enforce_tests = False

    def __init__(
        self,
        day: int,
        approach: str,
        *args,
        timeit: bool = False,
        read_file_as: Literal['raw', 'lines'] = 'raw',
        **kwargs,
    ):
        # Setup
        self.date = datetime.date(year=YEAR, month=12, day=day)
        self.text = f"Advent of Code, Day {self.date.day}, {self.__class__.__name__}"
        self.timeit = timeit
        self.read_file_as = read_file_as
        self.execution_time = None

        # The different approaches to the solutions we may use.
        self.approach = approach
        self.approaches = self._validate_approaches(self.approaches)
        self.args = [arg for arg in args]
        self.kwargs = {k: v for k,v in kwargs.items()}
        self.data = self._read_convert_and_clean_data()

    def clean(self, data):
        raise NotImplementedError("You should implement a method `clean(self, data)` to clean your data, or set the `clean_data` property to False.")

    def _validate_approaches(self, approaches: dict | None) -> dict:  # pyright: ignore
        """
        Validate the approaches dict.

        returns (example):
            approaches = {
                'approach name': {"func": self.the_function_to_call, "datatype": list},
            }
        """
        validated = {}
        try:
            assert self.approach, f"You should provide a valid approach ({self.approach=})."

            approaches: dict = {f"{self.approach}": getattr(self, self.approach)} if approaches is None and hasattr(self, self.approach) else {}

            for approach, func in approaches.items():
                # Get the function to call
                if func is not None:
                    assert hasattr(self, str(func.__name__)), f"Function for '{approach=}' not found."

                # Build the validated dict
                validated.update({f"{approach}": func})

        except AssertionError as e:
            message = "Implement valid approaches for the handler to work: approaches = {'approach name': {'func': 'functionname', Optional['datatype': list|set]} }"
            message += f"{message} - {e}"
            raise NotImplementedError(message)

        return validated

    def _path_from_filename(self, filename: str) -> Path:
        """Return the path to the file."""
        return Path(__file__).parent / filename if not any([c in filename for c in ('/', '\\')]) else Path(filename)

    def _read_convert_and_clean_data(self) -> list | set | str:
        """Read the data and convert it to the expected data_type (list, set or str)."""
        filename = self.filename if self.filename is not None else f"{self.date.day:02d}.data"
        data: list | str | set = read(path=self._path_from_filename(filename=filename), method=self.read_file_as)

        if self.clean_data:
            data = self.clean(data)
        return data

    def tests(self, results, *args, **kwargs) -> None:
        """
        Run the tests for the puzzle.

        -> assert some conditions that should be met.

        example:

            def tests(self, results):
                assert type(results) is int, f"The result of the function is not an integer. Got: {type(results)}"

        """
        ...

    def run_tests(self, results):
        """Run the tests for the puzzle."""
        own_methods = [name for name, item in type(self).__dict__.items() if isinstance(item, types.FunctionType)]
        if self.enforce_tests and 'tests' not in own_methods:
            try:
                raise NotImplementedError(f"You should implement a method `tests` to run the tests for the puzzle if 'enforce_tests' is True.\n{self.tests.__doc__}")
            except NotImplementedError as e:
                log.error(e)
        try:
            passed = self.tests(results=results)
            assert passed is None, f"Passing tests should not return anything. Got: {passed}"
        except AssertionError as error:
            log.error(f"Tests for puzzle: '{self.text}' using approach '{self.approach}' failed: '{error if error is not None else 'Assertion Text missing'}'")
        return results

    @property
    def result(self) -> Any:
        """
        Used as a convenience property for neater access.
        Usally, we can directly return the result.
        """
        return self.run_tests(self._calc_results_from_approaches(approach=self.approach, approaches=self.approaches, *self.args, **self.kwargs))

    @property
    def time(self) -> str:
        """Return a str of the execution time of the last run."""
        if self.execution_time is None:
            return "Did not time the execution of the last method call."
        return f"Execution time: {self.execution_time :0.4f} seconds."

    @staticmethod
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
    def _calc_results_from_approaches(self, approach, approaches, *args, **kwargs) -> Any:
        """Unpack the function from apporaches und call it."""
        assert approach in approaches, f"Not Found: {approach} is not a valid approach."
        run: Callable = approaches.get(approach)
        if run is None:
            raise NotImplementedError(f"Function for approach '{approach}' not found.")
        return run()
