from handler import Puzzle, approach, monitor

from typing import NamedTuple


class FileFree(NamedTuple):
    file: str
    free: str


class DiskFragmenter(Puzzle):
    clean_data = True

    def tests(self, results):
        assert self.calc_checksum('0099811188827773336446555566') == 1928, "wrong checksum"
        assert self.build_representation(self.clean("2333133121414131402")) == "00...111...2...333.44.5555.6666.777.888899", "wrong representation"
        assert self.defrag("0.0...") == "00....", "defrag failed"
        assert self.defrag("0.0.0.0") == "0000...", "defrag failed"

    def clean(self, data: str):
        data = data.strip('\n')
        files = [c for index, c in enumerate(data) if index % 2 == 0]
        frees = [c for index, c in enumerate(data) if index % 2 != 0]
        fragments = {}
        assert len(files) >= len(frees)
        for index, file in enumerate(files):
            try:
                fragments[index] = FileFree(file=file, free=frees.pop(0))
            except IndexError:
                fragments[index] = FileFree(file=file, free="0")
        return fragments

    def build_representation(self, fragments: dict):
        representation = ''
        sortd = {key: fragments[key] for key in sorted(fragments)}
        for key, value in sortd.items():
            representation += str(key) * int(value.file)
            representation += '.' * int(value.free)
        return representation

    def calc_checksum(self, line: str) -> int:
        _sum = 0
        stripped = line.rstrip(".")
        for i, c in enumerate(stripped):
            _sum += (int(c) * i)
        return _sum

    def identify_and_switch(self, representation: str) -> str:
        last_valid_char = representation.rstrip(".")[-1]
        last_valid_index = representation.rindex(last_valid_char)
        first_empty_index = representation.index('.')
        return self.switch(
            representation=representation,
            index_from=first_empty_index,
            index_to=last_valid_index
        )

    def switch(self, representation: str, index_from: int, index_to: int) -> str:
        representations = list(representation)
        representations[index_from], representations[index_to] = representations[index_to], representations[index_from]
        return "".join(representations)

    def defrag(self, representation: str) -> str:
        point_count = representation.rstrip(".").count(".")
        for _ in range(point_count + 1):
            leftovers = representation.rstrip(".")
            if "." not in leftovers:
                # No more points to move
                return representation
            # Otherwise, move the last char to the first point
            representation = self.identify_and_switch(representation)
        return representation

    @approach
    def checksum(self):
        representation = self.build_representation(self.data)
        defragged = self.defrag(representation)
        return self.calc_checksum(defragged)


DiskFragmenter(day=9, read='raw').info()
