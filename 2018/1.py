#!/usr/bin/env python3
# coding: utf-8

from itertools import accumulate, cycle

with open("1.data", "r") as file:
    data = file.read()

# data = [int(n.strip()) for n in data.split() if n.strip()]  # best-practice
data = data.replace("+", "")
data = data.split("\n")
data = [int(n) for n in data]

print("Task One:", sum(data))

frequencies = set()

print(
    "Task Two:",
    next(
        frequence
        for frequence in accumulate(cycle(data))
        if frequence in frequencies or frequencies.add(frequence)
    ),
)
