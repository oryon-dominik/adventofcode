#!/usr/bin/env python3
# coding: utf-8


from collections import Counter


def read_ranges_from_file(file="04.data"):
    """ read the range the password lies in from file """
    with open(file, "r") as ranges_file:
        ranges = ranges_file.read()
        ranges = [int(r) for r in ranges.split('-')]
    return ranges


def generate_password_task1(range_bottom, range_top):
    possible_passwords = []
    numbers = [str(n) for n in range(range_bottom, range_top) if "".join(sorted(str(n))) == str(n)]
    for number in numbers:
        # pop out numbers, that have no doubles
        count = Counter(number)
        if not all(n == 1 for n in list(count.values())):
            possible_passwords.append(int(number))
    return possible_passwords


def generate_password_task2(passwords):
    # TODO: not working yet
    possible_passwords = []
    for number in [str(n) for n in passwords]:
        # pop out numbers, that have no doubles
        count = list(Counter(number).values())
        match = False
        for n in count:
            if not n == 2 or n == 4 or n == 6:
                pass
            possible_passwords.append(int(number))
    return possible_passwords


range_bottom, range_top = read_ranges_from_file()
assert len(str(range_bottom)) == 6
assert len(str(range_top)) == 6

passwords = generate_password_task1(range_bottom, range_top)
print(f"Day 4, Task 1 found {len(passwords)} passwords meeting the criteria")

passwords = generate_password_task2(passwords)
print(f"Day 4, Task 2 found {len(passwords)} passwords meeting the criteria")

