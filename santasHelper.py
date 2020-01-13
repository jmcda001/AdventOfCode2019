from day1_TheTyrannyOfTheRocketEquation.fuel import part1 as day1part1, part2 as day1part2
from day2_1202ProgramAlarm.programAlarm import part1 as day2part1, part2 as day2part2
from day3_CrossedWires.wireJumble import part1 as day3part1, part2 as day3part2
from day4_SecureContainer.password import part1 as day4part1, part2 as day4part2
from day5_SunnywithaChanceofAsteroids.TEST import part1 as day5part1, part2 as day5part2
from day6_UniversalOrbitMap.universalOrbitMap import part1 as day6part1, part2 as day6part2
from day7_AmplificationCircuit.amplifier import part1 as day7part1, part2 as day7part2
from day8_SpaceImageFormat.imageDecode import part1 as day8part1, part2 as day8part2

inputFN = 'input.txt'
if __name__ == '__main__':
    day = 'day8_SpaceImageFormat/'
    print(day8part1(day+inputFN))

def test_day8():
    day = 'day8_SpaceImageFormat/'
    assert day8part1(day+inputFN) == 2159
    assert day8part2(day+inputFN) == '011000011011110100101110010010000100001010010100101000000010001001111010010100000001001000100101110010010100101000010010101000110001100111101001010010'

def test_day7(): 
    day = 'day7_AmplificationCircuit/'
    print(day7part1(day+inputFN))

def test_day6():
    day = 'day6_UniversalOrbitMap/'
    assert day6part1(day+inputFN) == 292387
    assert day6part2(day+inputFN) == 433

def test_day5():
    day = 'day5_SunnywithaChanceofAsteroids/'
    assert day5part1(day+inputFN) == 6069343
    assert day5part2(day+inputFN) == -1

def test_day4():
    assert day4part1() == 910
    assert day4part2() == 598

def test_day3():
    day = 'day3_CrossedWires/'
    assert day3part1(day+inputFN) == 1626
    assert day3part2(day+inputFN) == 27330

def test_day2():
    day = 'day2_1202ProgramAlarm/'
    assert day2part1(day+inputFN) == 3516593
    assert day2part2(day+inputFN) == 7749

def test_day1():
    day = 'day1_TheTyrannyOfTheRocketEquation/'
    assert day1part1(day+inputFN) == 3297909
    assert day1part2(day+inputFN) == 4943994
