#!/usr/bin/env python3
# coding: utf-8


def manhattan_distance(point: tuple, other_point: tuple) -> int:
    return abs(point[0] - other_point[0]) + abs(point[1] - other_point[1])


def read_wires_from_file(file="03.data"):
    """ read the two wire positions from fuel management system """
    with open(file, "r") as wires_file:
        wires = wires_file.readlines()
        first_wire = wire_to_coordinates([w.replace("\n", "") for w in wires[0].split(',')])
        second_wire = wire_to_coordinates([w for w in wires[1].split(',')])
    return first_wire, second_wire


def wire_to_coordinates(wire: list) -> list:
    wire_directions = []
    for w in wire:
        if w.startswith("R"):
            wire_directions.append((int(w[1:]), 0))
        elif w.startswith("L"):
            wire_directions.append((-int(w[1:]), 0))
        elif w.startswith("U"):
            wire_directions.append((0, int(w[1:])))
        elif w.startswith("D"):
            wire_directions.append((0, -int(w[1:])))
    return wire_directions


def points_a_wire_crosses(wire_directions):   
    wire_path, steps_lookup, movement_counter = [], {}, 0
    wire_position = origin = [0, 0]
    wire_path.append(tuple(wire_position))
    for point in wire_directions:
        for axe in (0, 1):  # x and y -coords
            if not point[axe] == 0:  # we have only one direction
                step = 1 if point[axe] > 0 else -1
                distance_with_direction = point[axe]
                for movement in range(step, distance_with_direction + step, step):
                    wire_position[axe] += step
                    movement_counter += 1
                    wire_path.append((tuple(wire_position)))
                    steps_lookup[tuple(wire_position)] = movement_counter
                    
    return wire_path, steps_lookup


def get_intersections(points: list, other_points: list):
    # [p for p in points if p in other_points]  # too slow!
    return list(set(points) & set(other_points))


# TESTS
fw = wire_to_coordinates(["R75","D30","R83","U83","L12","D49","R71","U7","L72"])
sw = wire_to_coordinates(["U62","R66","U55","R34","D71","R55","D58","R83"])
pwo, lookup1 = points_a_wire_crosses(fw)
pwt, lookup2 = points_a_wire_crosses(sw)
intersections = get_intersections(pwo, pwt)
distances = [manhattan_distance((0,0), i) for i in intersections if i != (0, 0)]
assert min(distances) == 159
# print('>>> DEBUG:', f'{lookup1[distances.index(min(distances))+ 1]}')
fw = wire_to_coordinates(["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"])
sw = wire_to_coordinates(["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"])
pwo, lookup1 = points_a_wire_crosses(fw)
pwt, lookup2 = points_a_wire_crosses(sw)
intersections = get_intersections(pwo, pwt)
distances = [manhattan_distance((0,0), i) for i in intersections if i != (0, 0)]
assert min(distances) == 135


# start program
first_wire, second_wire = read_wires_from_file()
points_wire_one, lookup_steps1 = points_a_wire_crosses(first_wire)
points_wire_two, lookup_steps2 = points_a_wire_crosses(second_wire)

print("Calculating Intersections..")
intersections = get_intersections(points_wire_one, points_wire_two)
# print("Intersections:", intersections)

steps = [lookup_steps1[i] + lookup_steps2[i] for i in intersections if i != (0, 0)]
print(f"Day 3, Task 2 the minimum steps are: {min(steps)}")

print("Calculating distances..")
distances = [manhattan_distance((0,0), i) for i in intersections if i != (0, 0)]

md = min(distances) if distances != [] else 'no intersections'
print(f"Day 3, Task 1 the minimal manhattan distance of an intersection is: {md}")
