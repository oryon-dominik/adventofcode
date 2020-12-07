#!/usr/bin/env python3
# coding: utf-8


""" First I tried to mess with metaclasses, but this was a trap, for now :P
# class Metaclass(type):
#     def __new__(cls, clsname, bases: tuple, attrs:dict):
#         # change some meta-stuff before creating the class here
#         return super().__new__(cls, clsname, bases, attrs)


# class PlanetaryObject(object, metaclass=COM):
#     pass
"""


from typing import Optional



def read_orbit_data_from_file(file="06.data") -> list:
    """ read the orbits from file """
    with open(file, "r") as orbits_file:
        orbit_relations = orbits_file.readlines()
    orbit_relations = [r.replace("\n", "") for r in orbit_relations]
    # print(f'>>> DEBUG: {orbits}')
    return orbit_relations


def create_and_sort_classes(relations: list) -> dict:
    """ creates all classes in relations and returns a lookup-dictionary"""
    classes, unsorted = create_classes_split_unsorted(relations)
    while unsorted != []:
        classes, unsorted = create_classes_split_unsorted(unsorted, classes)
    return classes


def create_classes_split_unsorted(
    orbit_relations: list, orbit_classes: dict = None, center_of_mass="COM"
):
    """ creates classes(with subclasses) -> classes_dict, unsorted_relations_list
    
        for all planetary 'orbit-relations' that directly derive from
        center_of_mass or a direct ancessor a class is created and returned in
        'orbit_classes'
    
        unsorted orbit_relations that can not be derived directly (they are not
        present in the 'orbit_classes' lookup-dict yet) are returned
    """
    assert all([type(o) == str for o in orbit_relations])
    unsorted_relations = []
    if orbit_classes is None:
        orbit_classes = {}
    for r in orbit_relations:
        origin_str, orbit_str = r.split(")")
        # create origin if not existent
        if origin_str == center_of_mass:
            origin = create_origin_class(origin_str)
            orbit_classes["origin"] = origin  # TBD: do we need this?
            orbit_classes[origin_str] = origin
        if not orbit_classes.get(origin_str, None):
            # unsorted element,
            unsorted_relations.append(r)
            continue
        # create orbit
        base_class = orbit_classes[origin_str]
        # all sub-classes are in the method-resolution-order:
        bases = tuple(t for t in type.mro(base_class))
        orbit = create_orbit_class(orbit_str, bases, {"name": orbit_str})
        orbit_classes[orbit_str] = orbit
    return orbit_classes, unsorted_relations


def create_origin_class(origin: str):
    """ creates a class without parents """
    attrs = {"name": origin}
    return type(origin, (), attrs)


def create_orbit_class(class_name: str, parents: tuple, attributes: dict = None):
    """ createas a class with parents (base-classes)
        (re-)sets the name-atrtribute to class_name """

    """ not needed for now:
    # overwrite the class' name attribute
    if attributes is None:
        attributes = {}
    attributes["name"] = class_name
    # remove the class' name attribute
    name = attributes.get('name', None)
    if name is not None:
        del attributes['name']
    """
    # return a class-object (not an instance of the class!)
    return type(class_name, parents, attributes)  # can create classes


def number_of_orbits(object_) -> int:
    """ returns the number of objects the 'object_' (a class) orbits around
        - 1 because the object circles around herself :) """
    return len(object_.__bases__) - 1


def total_number_of_direct_and_indirect_orbits(systems: dict) -> int:
    """ sum up for orbit_count_checksum """
    return sum([number_of_orbits(o) for key, o in systems.items()])


def last_intersection_of_way_to_two_systems(system_one, system_two) -> Optional[object]:
    """ returns last intersection or None, when not intersecting """
    intersections = [b for b in system_one.__bases__ if b in system_two.__bases__]
    if intersections:
        last_instersection = sorted(
            intersections,
            key=lambda x: number_of_orbits(x),
            reverse=True
        )[0]  # <- the first element is our matching intersection
        return last_instersection


def transfer_count_from_to(class_one, class_two) -> int:
    """ calculates the minimum number of orbital transfers required to move from
    the object class_one is orbiting to the object class_two is orbiting

    distances are reduced by one, because the objects are moving themselves, so
    they mustn't be taken into (ac)count
    """
    distance_reduced = 0  # if no intersection exists, go the whole way
    last_intersection = last_intersection_of_way_to_two_systems(class_one, class_two)
    if last_intersection is not None:
        distance_reduced = number_of_orbits(last_intersection)
    distance_one = number_of_orbits(class_one) - 1
    distance_two = number_of_orbits(class_two) - 1
    return (distance_one - distance_reduced) + (distance_two - distance_reduced)


# TESTS
test_input = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n")
systems = create_and_sort_classes(test_input)
orbit_count_checksum = total_number_of_direct_and_indirect_orbits(systems)
assert orbit_count_checksum == 42
test_input2 = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN".split("\n")
systems = create_and_sort_classes(test_input2)
assert transfer_count_from_to(systems['YOU'], systems['SAN']) == 4


# start the program
orbit_relations = read_orbit_data_from_file()
systems = create_and_sort_classes(orbit_relations)
orbit_count_checksum = total_number_of_direct_and_indirect_orbits(systems)

print(
    "Day 6, Task 1 - "
    "The total number of direct and indirect orbits (checksum) is: "
    f"{orbit_count_checksum}"
    )
print(
    "Day 6, Task 2 - "
    "The Minimum Distance from YOU to SAN is: "
    f"{transfer_count_from_to(systems['YOU'], systems['SAN'])}"
    )
