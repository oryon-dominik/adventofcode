import pytest
from importlib import import_module
from pathlib import Path


@pytest.fixture
def puzzle():
    day = import_module("2022.07", package=str((Path.cwd()).resolve()))
    yield day.NoSpaceLeftOnDevice(day=7, read='raw')

@pytest.fixture
def directory_e():
    yield "584 file"

def test_content_size(puzzle, directory_e):
    assert puzzle.content_size(content=directory_e) == 584
