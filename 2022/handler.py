import functools
import time
import datetime
import types
import tracemalloc
import inspect
import sys
from pathlib import Path
from copy import deepcopy

from typing import Literal, Any, Callable
from logs import log
from inout import read
from typing import NamedTuple

import humanize


class ExecutionStats(NamedTuple):
    name: str
    time: float
    memory: str


YEAR = 2022


def recursionlimit(depth: int, verbose: bool = True):
    def _adjust_recursion_limit(depth: int = 1_000, reset=False, recursion_cache={}):
        """
        Adjust the recursion limit to the maximum possible.
        """
        if recursion_cache.get('current') is None:
            recursion_cache['current'] = sys.getrecursionlimit()  # usally 1000
        if not reset:
            sys.setrecursionlimit(depth)
        else:
            sys.setrecursionlimit(recursion_cache['current'])

    def decorator(func: Callable):
        """
        Decorator to adjust the recursion limit to depth provided.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _adjust_recursion_limit(depth=depth)
            value = func(*args, **kwargs)
            _adjust_recursion_limit(reset=True)
            return value
        return wrapper
    if verbose:
        log.warn('Adjusting the recursionlimit may impose the risk of a stack overflow/segfault!')
    return decorator

def approach(func: Callable):
    """
    Decorator to add approaches to the handler. Literally just does nothing
    but adding the @approach to the source code :P
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        value = func(self, *args, **kwargs)
        return value
    return wrapper

def monitor(func: Callable):
    """Decorator to add monitoring stats to the execution of a function."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.timeit:
            # Don't time the execution, just return the result
            return func(self, *args, **kwargs)
        # Time it. Execute. Return.
        time_start = time.perf_counter()
        # Memory usage
        tracemalloc.start()
        value = func(self, *args, **kwargs)
        time_end = time.perf_counter()
        execution_time = time_end - time_start
        self.statistics.insert(0, ExecutionStats(
            name=func.__name__,
            time=execution_time,
            memory=humanize.naturalsize(tracemalloc.get_traced_memory()[-1]))
        )
        tracemalloc.stop()
        return value
    return wrapper


class Puzzle:
    clean_data = False
    filename = None
    enforce_tests = False

    def __init__(
        self,
        day: int,
        *args,
        timeit: bool = True,
        read: Literal['raw', 'lines'] = 'lines',
        mode: Literal['r', 'rb'] = 'r',
        **kwargs,
    ):
        # Setup
        self.date = datetime.date(year=YEAR, month=12, day=day)
        self.text = f"Advent of Code, Day {self.date.day}, {self.__class__.__name__}"
        self.timeit = timeit
        self.read = read
        self.mode = mode
        self.statistics = []

        self.approaches = self._validate_approaches()

        self.args = [arg for arg in args]
        self.kwargs = {k: v for k,v in kwargs.items()}
        self.data = self._read_convert_and_clean_data()

    def clean(self, data):
        raise NotImplementedError("You should implement a method `clean(self, data)` to clean your data, or set the `clean_data` property to False.")

    @classmethod
    def _approaches(cls) -> list:
        """The approaches to the puzzle are decorated functions."""
        source = inspect.getsourcelines(cls)
        locs = [source[0][i + 1] for i, value in enumerate(source[0]) if "@approach" in value]
        decorated = [loc.strip().split('(')[0].removeprefix('def ') for loc in locs]
        return decorated

    def _validate_approaches(self) -> dict:  # pyright: ignore
        """
        Validate the approaches dict.

        returns (example):
            approaches = {
                'approach name': {"func": func},
            }
        """
        validated = {}
        try:

            approaches: dict = {f"{approach}": getattr(self, approach) for approach in self.__class__._approaches()}

            for approach, func in approaches.items():
                # Get the function to call
                if func is not None:
                    assert hasattr(self, str(func.__name__)), f"Function for '{approach=}' not found."

                # Build the validated dict
                validated.update({f"{approach}": {"func": func, "statistics": []}})

        except AssertionError as e:
            message = "Implement valid approaches for the handler to work: approaches = {'approach name': {'func': func} }"
            message += f"{message} - {e}"
            raise NotImplementedError(message)
        return validated

    def _path_from_filename(self, filename: str) -> Path:
        """Return the path to the file."""
        return Path(__file__).parent / filename if not any([c in filename for c in ('/', '\\')]) else Path(filename)

    def tests(self, results: Any, *args, **kwargs) -> None:
        """
        Run the tests for the puzzle.

        -> assert some conditions that should be met.

        example:

            def tests(self, results):
                assert type(results) is int, f"The result of the function is not an integer. Got: {type(results)}"

        """
        ...

    def run_tests(self, results, approach: str):
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
            log.error(f"Tests for puzzle: '{self.text}' using approach '{approach}' failed: '{error if error is not None else 'Assertion Text missing'}'")
        return results

    def result(self, approach: str, func: Callable) -> Any:
        """
        Used as a convenience property for neater access.
        Usally, we can directly return the result.
        """
        return self.run_tests(results=self._calc_results(func, *self.args, **self.kwargs), approach=approach)

    @property
    def datacopy(self):
        """Return a copy of the puzzles data."""
        return deepcopy(self.data)

    def data_reread_changes(self) -> bool:
        """Reread the data and return True if the data has changed."""
        copied = self.datacopy
        self.data = self._read_convert_and_clean_data()
        return self.data != copied

    def _camelize(self, approach: str) -> str:
        return "".join(word.capitalize() for word in approach.split('_'))

    def info(self):
        for approach, values in self.approaches.items():
            log.info(f"{self.text} | {self._camelize(approach)}: {self.result(approach, values['func'])} | {self.stats}")

    @property
    def stats(self) -> str:
        """Return a str of the execution stats of the last run."""
        additional_monitors = [stat for stat in self.statistics if stat.name != '_calc_results']
        self.statistics = [stat for stat in self.statistics if stat.name == '_calc_results']
        if self.statistics == [] and additional_monitors == []:
            return "Did not time statistics of the last method calls."
        adds = ''.join(f"\nExecution time for '{am.name}': {am.time :0.4f} seconds. | Consumed memory: {am.memory}." for am in additional_monitors)
        if self.statistics == [] and additional_monitors != []:
            return adds
        et = self.statistics.pop()
        return f"Execution time{f' for {et.name}' if not et.name.startswith('_')else ' for results'}: {et.time :0.4f} seconds. | Consumed memory: {et.memory}.{adds}"

    def _read_convert_and_clean_data(self) -> list | set | str:
        """Read the data and convert it to the expected data_type (list, set or str)."""
        filename = self.filename if self.filename is not None else f"{self.date.day:02d}.data"
        data: list | str | set = read(path=self._path_from_filename(filename=filename), method=self.read, mode=self.mode)

        if self.clean_data:
            data = self.clean(data)
        return data

    @monitor
    def _calc_results(self, run: Callable, *args, **kwargs) -> Any:
        """Unpack the function from apporaches und call it."""
        return run(*args, **kwargs)
