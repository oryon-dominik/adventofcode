import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(SCRIPT_DIR))

from handler import Puzzle, approach, recursionlimit


MARKER_LENGTH = 4
MESSAGE_MARKER_LENGTH = 14


class TuningTrouble(Puzzle):

    def tests(self, results):
        # Tests one
        assert len(self.find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", length=MARKER_LENGTH)) + MARKER_LENGTH == 5, "Test 1 failed"
        assert len(self.find_marker("nppdvjthqldpwncqszvftbrmjlhg", length=MARKER_LENGTH)) + MARKER_LENGTH == 6, "Test 2 failed"
        assert len(self.find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", length=MARKER_LENGTH)) + MARKER_LENGTH == 10, "Test 3 failed"
        assert len(self.find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", length=MARKER_LENGTH)) + MARKER_LENGTH == 11, "Test 4 failed"
        # Tests two
        assert len(self.find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", length=MESSAGE_MARKER_LENGTH)) + MESSAGE_MARKER_LENGTH == 19, "Test 5 failed"

    def reduce_till_finding_unique_marker(self, string: str, length: int = MARKER_LENGTH, offset: int = 1):
        """
        Find the first instance of a marker in a string.
        """
        if len(set(string[:length])) == length:
            return string
        return self.reduce_till_finding_unique_marker(string=string[offset:], length=length)

    @recursionlimit(depth=3_850)
    def find_marker(self, data: str, length: int) -> str:
        string = self.reduce_till_finding_unique_marker(string=data, length=length)
        return data.removesuffix(string)

    @approach
    def detect_packet_marker_start(self) -> int:
        self.datacopy: str
        result = self.find_marker(data=self.datacopy, length=MARKER_LENGTH)
        return len(result) + MARKER_LENGTH

    @approach
    def detect_message_marker_start(self) -> int:
        self.datacopy: str
        result = self.find_marker(data=self.datacopy, length=MESSAGE_MARKER_LENGTH)
        return len(result) + MESSAGE_MARKER_LENGTH


if __name__ == '__main__':
    advent = TuningTrouble(day=6, read='raw')
    advent.info()
