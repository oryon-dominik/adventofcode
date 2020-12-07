#!/usr/bin/env python3
# coding: utf-8


with open('5.data', 'r') as file:
    polymer = [line.strip() for line in file.readlines()][0]

chars = 'abcdefghijklmnopqrstuvwxyz'

def react(polymer):
    for char in chars:
        polymer = polymer.replace(f'{char}{char.upper()}', '')
        polymer = polymer.replace(f'{char.upper()}{char}', '')
    return polymer

still_reacting = polymer
still_reacting = react(still_reacting)

while polymer is not still_reacting:
    polymer = still_reacting
    still_reacting = react(still_reacting)

print('Task One:', len(polymer))

replaced_polymers = {}

for char in chars:
    reaction = polymer
    reaction = reaction.replace(f'{char}', '')
    reaction = reaction.replace(f'{char.upper()}', '')

    still_reacting = reaction
    still_reacting = react(still_reacting)

    while reaction is not still_reacting:
        reaction = still_reacting
        still_reacting = react(still_reacting)

    replaced_polymers[char] = len(reaction)

print('Task Two:', replaced_polymers[min(replaced_polymers, key=replaced_polymers.get)])
