#!/usr/bin/env python3
# coding: utf-8


import re
from collections import Counter


def date_sort(datelist):
    date_time = datelist.split(' ')
    splitup = date_time[0].split('-')
    return splitup[0], splitup[1], splitup[2], date_time[1]


with open('4.data', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

lines.sort(key=lambda x: date_sort(x))
guards = {}
start, stop, current_guard = 0, 0, 0

for line in lines:
    values = re.findall("\d+", line)
    if "Guard" in line:
        current_guard = int(values[-1])
    elif "falls asleep" in line:
        start = int(values[-1])
    elif "wakes up" in line:
        stop = int(values[-1])
        for i in range(start, stop):
            guards.setdefault(current_guard, []).append(i)

# part 1
id1 = max(guards, key=lambda x: len(guards[x]))
c = Counter(guards[id1])
minute = c.most_common()[0][0]
print(id1 * minute)

# part2
id2 = max(guards, key=lambda x: Counter(guards[x]).most_common()[0][1])
print(id2 * Counter(guards[id2]).most_common()[0][0])
