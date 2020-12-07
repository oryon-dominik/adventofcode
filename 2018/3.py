#!/usr/bin/env python3
# coding: utf-8

with open('3.data', 'r') as file:
    data = [line.strip() for line in file.readlines()]

def string_processing(elf_data):
    params = elf_data.split()
    elf_id = params[0][1:]
    x = int(params[2].split(',')[0]) - 1
    y = int(params[2].split(',')[1][:-1]) - 1
    width = int(params[3].split('x')[0])
    height = int(params[3].split('x')[1])
    return elf_id, x, y, width, height

elves = {}

for elf in data:
    elf_id, x, y, width, height = string_processing(elf)
    elves[f'{elf_id}'] = {
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'overlap': False,
    }

board = [['.' for x in range(1000)] for y in range(1000)]

recheck = []

for elf, values in elves.items():
    overlap = False
    x1 = values['x']
    x2 = x1 + values['width']
    y1 = values['y']
    y2 = y1 + values['height']

    for y in range(y1, y2):
        for x in range(x1, x2):
            if board[y][x] == '.':
                board[y][x] = 'X'
            elif board[y][x] == 'X':
                board[y][x] = '2'
                overlap = True
            elif board[y][x] == '2':
                overlap = True
            else:
                print('ERROR')
    if overlap:
        values['overlap'] = True
    else: recheck.append(elf)

for elf in recheck:
    x1 = elves[elf]['x']
    x2 = x1 + elves[elf]['width']
    y1 = elves[elf]['y']
    y2 = y1 + elves[elf]['height']

    for y in range(y1, y2):
        for x in range(x1, x2):
            if board[y][x] is not 'X':
                elves[elf]['overlap'] = True

exceeded_claims = 0

for row in board:
    for column in row:
        if column == '2':
            exceeded_claims += 1

print('Task One:', exceeded_claims)

no_overlapping = [elf for elf, values in elves.items() if not values['overlap']]

print('Task Two:', no_overlapping)
