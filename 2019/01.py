#!/usr/bin/env python3
# coding: utf-8


from pathlib import Path


def calc_mass(fuel):
    return fuel


def fuel_required(mass: int):  # to reach the stars
    fuel = (int(mass / 3)) - 2
    return fuel


def fuel_required_with_transport_fuel(mass: int):  # to reach the stars, take transport fuel into concern
    fuel = (int(mass / 3)) - 2
    additional_mass = calc_mass(fuel)
    while additional_mass > 0:
        transport_fuel = fuel_required(additional_mass)
        additional_mass = calc_mass(transport_fuel)
        if transport_fuel > 0:
            fuel += transport_fuel
    return fuel


def read_masses_from_file(file_="01.data"):
    """ read the measurements from fifty stars """
    with open(file_, "r") as star_masses_file:
        masses = star_masses_file.readlines()
        masses = [m.replace("\n", "") for m in masses]
    return masses


# calc the fuel required to reach the 50 stars
fuel_required_to_reach_the_stars = sum([fuel_required(int(m)) for m in masses])

print(f"Day 1, Task1 we need this amount of fuel: {fuel_required_to_reach_the_stars}")

fuel_total = sum([fuel_required_with_transport_fuel(int(m)) for m in masses])

print(f"Day 1, Task2 we need this amount of total fuel: {fuel_total}")
