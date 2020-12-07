from puzzle_handler import AdventPuzzleHandler
import math


class TobogganTrajectory(AdventPuzzleHandler):

    approaches = {
            'simple_index_count': {"func": "simple_index_count", "datatype": list},
            'multiple_slopes': {"func": "multiple_slopes", "datatype": list},
        }
    puzzle_day = 3
    clean_data = False

    def build_map(self, data, slope):
        tree_map = []
        # okay we'll need a full map.. 
        # given it's x-axis is slope[y]/slope[x] times larger then the y-axis..
        gradient = slope[1] / slope[0]
        y_length, x_length = len(data), len(data[0]) if len(data) > 0 else 0
        supposed_x_length = y_length * gradient
        multipy_with = supposed_x_length / x_length
        # we can just use full-ints here, and we round up (or down) to get a larger map then needed
        # (and to not get any errors later)
        size = int(math.ceil(multipy_with))
        for row in data:
            tree_map.append(row * size)
        return tree_map

    def ride_the_toboggan(self, tree_map, slope):
        # count how many trees we hit
        trees_hit = 0
        # start top left
        x_position = 0
        
        if slope[1] / slope[0] < 1:
            # we traverse the map for easy traversal, if the slope is moving more y then x
            tree_map = ["".join(trees) for trees in zip(*tree_map)]
            slope = slope[1], slope[0]

        # traversing the tree filled snow field..
        for y_position, row in enumerate(tree_map):
            try:
                if row[x_position] == '#':
                    trees_hit += 1
                x_position += slope[1]
            except IndexError:
                # we sucessfully passed the forest, no tree here.
                pass
        return trees_hit

    def build_a_map_and_ride_the_togo(self, slope):
        tree_map = self.build_map(self.data, slope)
        return self.ride_the_toboggan(tree_map, slope)

    def simple_index_count(self) -> int:
        """we just simply count the indices (trees hit)"""
        slope = 1, 3
        return self.build_a_map_and_ride_the_togo(slope)

    def multiple_slopes(self) -> int:
        slopes = [
            (1, 1),
            (1, 3),
            (1, 5),
            (1, 7),
            (2, 1),
        ]
        trees_hit = []
        for slope in slopes:
            trees_hit.append(self.build_a_map_and_ride_the_togo(slope))
        return math.prod(trees_hit)


ride_on_the_tobo = TobogganTrajectory(timeit=True, approach="simple_index_count")
print(f"{ride_on_the_tobo.text} | Task1 - SIMPLE_COUNT riding the toggoban: {ride_on_the_tobo.result} - {ride_on_the_tobo.time}")

ride_on_the_tobo = TobogganTrajectory(timeit=True, approach="multiple_slopes")
print(f"{ride_on_the_tobo.text} | Task2 - MULTIPLE_SLOPES riding the toggoban: {ride_on_the_tobo.result} - {ride_on_the_tobo.time}")
