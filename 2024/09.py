from handler import Puzzle, approach, monitor

from typing import NamedTuple


class FileFree(NamedTuple):
    file: str
    free: str


class DiskFragmenter(Puzzle):
    clean_data = True

    def clean(self, data: str):
        data = data.strip('\n')
        # data.lstrip('\n')
        files = [c for index, c in enumerate(data) if index % 2 == 0]
        frees = [c for index, c in enumerate(data) if index % 2 != 0]
        fragments = {}
        for index, file in enumerate(files):
            try:
                fragments[index] = FileFree(file=file, free=frees.pop(0))
            except IndexError:
                fragments[index] = FileFree(file=file, free='0')
        return fragments

    def build_representation(self, fragments: dict):
        representation = ''
        for key, value in fragments.items():
            representation += str(key) * int(value.file)
            representation += '.' * int(value.free)
        return representation

    def tests(self, results):
        assert self.calc_checksum('0099811188827773336446555566') == 1928, "wrong checksum"
        assert self.build_representation(self.clean("2333133121414131402")) == "00...111...2...333.44.5555.6666.777.888899", "wrong representation"
        assert self.is_finished("0.0...") is False, "not finished"
        assert self.is_finished("00...") is True, "finished"
        assert self.defrag("0.0...") == "00....", "defrag failed"
        assert self.defrag("0.0.0.0") == "0000...", "defrag failed"

    def calc_checksum(self, line: str) -> int:
        _sum = 0
        stripped = line.rstrip(".")
        for i, c in enumerate(stripped):
            _sum += int(c) * i
        return _sum

    def is_finished(self, representation: str) -> bool:
        return "." not in representation.rstrip('.')

    def defrag(self, representation: str) -> str:
        point_count = representation.count('.')
        for _ in range(point_count):
            leftovers = representation.rstrip(".")
            last_char = leftovers[-1]
            replace_index = representation.index('.')
            last_index = representation.rindex(last_char)
            if last_index >= replace_index:
                representation = representation[:replace_index] + last_char + representation[replace_index + 1:]
                representation = representation[:last_index] + '.' + representation[last_index + 1:]
        return representation

    @approach
    def checksum(self):
        representation = self.build_representation(self.data)
        # while not self.is_finished(representation):
        representation = self.defrag(representation)
        return self.calc_checksum(representation)


DiskFragmenter(day=9, read='raw').info()
