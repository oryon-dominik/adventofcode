#!/usr/bin/env python3
# coding: utf-8

def get_asteroid_positions(starmap: str) -> list:
    asteroids = []
    starmap = starmap.strip()
    lines = starmap.split('\n')
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                asteroids.append((x, y))
    asteroids
    return asteroids


def give_me_a_slope(asteroid1, asteroid2):
    slope = None
    x1, y1 = asteroid1
    x2, y2 = asteroid2
    if x2 == x1:
        slope = "infinity"
        return None
    if slope != "infinity":
        number = (y2 - y1) / (x2 - x1)
        return number


def calc_intercept(asteroid, slope):
    x, y = asteroid
    if slope is not None:
        intercept = -1 * (slope * x - y)
        return intercept
    return None


def count_sight_lines(homebase, asteroids):
    sight_lines = len(asteroids) - 1  # don't count self
    homebase_lines = {}
    other_asteroids = [a for a in asteroids if a is not homebase]
    for other_asteroid in other_asteroids:
        slope = give_me_a_slope(homebase, other_asteroid)
        intercept = calc_intercept(other_asteroid, slope)
        homebase_lines[other_asteroid] = {
            "slope": slope,
            "intercept": intercept,
            "sight": sight_lines
            }

    sights = {}
    for asteroid, line in homebase_lines.items():
        sight_lines = len(asteroids) - 1  # reset
        if line['slope'] is not None and line['intercept'] is not None:
            for other_asteroid in other_asteroids:
                if other_asteroid != asteroid:  # don't check for itself
                    # does the other asteroid cross the line too ?
                    hx, hy = homebase
                    # print('>>> DEBUG: hx, hy, slope', hx, hy, slope, intercept)
                    x, y = other_asteroid
                    equation_other_asteroid = round(x * line['slope'] + line['intercept'], 6)
                    if equation_other_asteroid == round(y, 6):
                        if x < asteroid[0] < homebase[0] or x > asteroid[0] > homebase[0]:
                            sight_lines -= 1
        else:
            for other_asteroid in other_asteroids:
                if other_asteroid != asteroid:
                    # x values are the same:
                    x, y = other_asteroid
                    if y < asteroid[1] < homebase[1] or y > asteroid[1] > homebase[1]:
                            sight_lines -= 1

        sights[asteroid] = sight_lines

    # how many asteroids cross that line
    return sights


def build_dict(asteroids):
    asteroids_dict = {}
    for asteroid in asteroids:
        asteroid_sights = count_sight_lines(asteroid, asteroids)
        maximum = asteroid_sights[max(asteroid_sights)]
        asteroids_dict[asteroid] = maximum

    return asteroids_dict


def get_best_position(asteroids_dict):
    return max(asteroids_dict, key=asteroids_dict.get)

# =================================
# TESTS

test_input = """
.#..#
.....
#####
....#
...##
"""

"""
.7..7
.....
67775
....7
...87
"""


test_position = (3,4)
test_sees = 8

asteroids = get_asteroid_positions(test_input)
asts = build_dict(asteroids)
best_position = get_best_position(asts)
print(f'>>> DEBUG: {asts}')
print(f"{best_position}")
print(f"{test_position}")

#assert best_position == test_position
can_see = asts[best_position]
#assert can_see == test_sees


test_input = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""


test_input = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

test_position = (1,2)
test_sees = 35

asteroids = get_asteroid_positions(test_input)
asts = build_dict(asteroids)
best_position = get_best_position(asts)
print(f'>>> DEBUG: {asts}')
print(f"{best_position}")
print(f"{test_position}")

#assert best_position == test_position
can_see = asts[best_position]
#assert can_see == test_sees






test_input = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

test_position = (6, 3)
test_sees = 41

test_input = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

test_position = (11, 13)
test_sees = 210

asteroids = get_asteroid_positions(test_input)
asts = build_dict(asteroids)
best_position = get_best_position(asts)
print(f'>>> DEBUG: {asts}')
print(f"{best_position}")
print(f"{test_position}")

#assert best_position == test_position
can_see = asts[best_position]
print('>>> DEBUG: ', can_see)
assert can_see == test_sees