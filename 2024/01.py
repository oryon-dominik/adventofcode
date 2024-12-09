from handler import Puzzle, approach


class DistanceLists(Puzzle):
    clean_data = True

    def clean(self, data: str):
        entries = [n.split() for n in data.split('\n') if n]
        xs = []
        ys = []
        for e in entries:
            x, y = e
            xs.append(int(x))
            ys.append(int(y))
        zipped = zip(sorted(xs), sorted(ys))
        distances = [abs(abs(x) - abs(y)) for x, y in zipped]
        return distances

    @approach
    def total_distance(self):
        self.data: list
        return sum(self.data)


DistanceLists(day=1, read='raw').info()
