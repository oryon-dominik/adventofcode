import pytest
from importlib import import_module
from pathlib import Path


handler_2022 = import_module("2022.handler", package=str((Path.cwd()).resolve()))

@pytest.fixture
def puzzle_year_2022():
    yield handler_2022.YEAR
