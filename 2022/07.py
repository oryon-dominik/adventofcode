import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(SCRIPT_DIR))

from handler import Puzzle, approach, recursionlimit



class NoSpaceLeftOnDevice(Puzzle):

    def content_size(self, content: str) -> int:
        return int(content.split(' ')[0])

    @approach
    def solve(self) -> Any:
        ...


if __name__ == '__main__':
    advent = NoSpaceLeftOnDevice(day=7, read='raw')
    advent.info()
