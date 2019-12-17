from day1_TheTyrannyOfTheRocketEquation.fuel import part1 as day1part1, part2 as day1part2
from day2_1202ProgramAlarm.programAlarm import part1 as day2part1, part2 as day2part2
from day3_CrossedWires.wireJumble import part1 as day3part1, part2 as day3part2
from day4_SecureContainer.password import part1 as day4part1, part2 as day4part2
from day5_SunnywithaChanceofAsteroids.TEST import part1 as day5part1, part2 as day5part2

inputFN = 'input.txt'
if __name__ == '__main__':
    pass

def test_day5():
    day = 'day5_SunnywithachanceofAsteroids/'
    assert day5part1(day+inputFN) == 6069343
    # TODO: Solve part 2
    assert day5part2(day+inputFN) == None

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
