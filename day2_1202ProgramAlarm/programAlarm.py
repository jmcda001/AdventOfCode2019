from IntcodeComputer.intcode import Program
from typing import List
import copy

def runProgram(program: List[int])->List[int]:
    p = Program(program)
    p.run()
    return p.instructions

def part1(fn: str):
    with open(fn) as f:
        program = [int(i) for i in f.readline().split(',')]
        noun = 12
        verb = 2
        program[1] = noun
        program[2] = verb
        output = runProgram(program)
        print(f'Output at index 0 after running modified program is {output[0]}')
        return output[0]

def part2(fn: str):
    with open(fn) as f:
        program = [int(i) for i in f.readline().split(',')]
        noun = 12
        verb = 2
        target = 19690720
        while True:
            program[1] = noun
            output = runProgram(copy.deepcopy(program))
            if output[0] > target:
                noun -= 1
                break
            noun += 1
        program[1] = noun
        verb = target - runProgram(copy.deepcopy(program))[0]
        program[2] = verb
        output = runProgram(program)
        print(f'Output at index 0 after running modified program is {output[0]}')
        print(f'100 * noun + verb? {100 * noun + verb}')
        return 100 * noun + verb

def test_runProgram():
    testInput = [1,0,0,0,99]
    expected = [2,0,0,0,99]
    output = runProgram(testInput)
    assert output == expected
    
    testInput = [2,3,0,3,99]
    expected = [2,3,0,6,99]
    output = runProgram(testInput)
    assert output == expected
    
    testInput = [2,4,4,5,99,0]
    expected = [2,4,4,5,99,9801]
    output = runProgram(testInput)
    assert output == expected
    
    testInput = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    output = runProgram(testInput)
    assert output == expected
    
