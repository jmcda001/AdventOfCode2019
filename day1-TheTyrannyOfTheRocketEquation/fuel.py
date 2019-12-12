import math
from typing import List

def withoutFuelWeight(masses: List[int]) -> int:
    fuelSum = 0
    for mass in masses:
        fuelSum += math.floor(mass / 3) - 2
    return fuelSum

def withFuelWeight(masses: List[int]) -> int:
    fuelSum = 0
    for mass in masses:
        moduleMass = mass
        while True:
            fuelNeeded = math.floor(moduleMass / 3) - 2
            moduleMass = fuelNeeded
            if fuelNeeded <= 0:
                break
            fuelSum += fuelNeeded
    return fuelSum

with open("input.txt") as f:
    masses = [int(m) for m in f.readlines()]
    print(f'Fuel needed (without fuel mass):\t{withoutFuelWeight(masses)}')
    print(f'Fuel needed (with fuel mass):\t\t{withFuelWeight(masses)}')
        
