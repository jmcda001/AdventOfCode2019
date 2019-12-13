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
	
if __name__ == '__main__':
    with open("input.txt") as f:
        masses = [int(m) for m in f.readlines()]
        print(f'Fuel needed (without fuel mass):\t{withoutFuelWeight(masses)}')
        print(f'Fuel needed (with fuel mass):\t\t{withFuelWeight(masses)}')

def test_withoutFuelWeight():
    assert withoutFuelWeight([12]) == 2
    assert withoutFuelWeight([14]) == 2
    assert withoutFuelWeight([1969]) == 654
    assert withoutFuelWeight([100756]) == 33583

def test_withFuelWeight():
    assert withFuelWeight([14]) == 2
    assert withFuelWeight([1969]) == 966
    assert withFuelWeight([100756]) == 50346
