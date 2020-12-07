#!/usr/bin/env python3
# coding: utf-8

with open("2.data", "r") as file:
    data = [line.strip() for line in file.readlines()]

count_two = 0
count_three = 0

for box in data:
    for letter in box:
        if box.count(letter) == 2:
            count_two += 1
            break

    for letter in box:
        if box.count(letter) == 3:
            count_three += 1
            break

print("Task One:", count_two * count_three)

for box in data:
    for other_box in data:
        samechars = [
            char for char, other_char in zip(box, other_box) if char == other_char
        ]
        if len(box) - 1 == len(samechars):
            commons = "".join(samechars)
            break

print("Task Two:", commons)
