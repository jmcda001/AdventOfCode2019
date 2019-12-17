from typing import List
import copy

opcodes = {1: (lambda p,i: p[p[i+1]]+p[p[i+2]]),
    2: (lambda p,i: p[p[i+1]]*p[p[i+2]]),
}

def runProgram(program: List[int])->List[int]:
    pc = 0
    ADV = 4
    while pc < len(program) and program[pc] != 99:
        op = program[pc]
        if op not in opcodes:
            print(f'Error: Encountered unknown opcode {op} at index {pc}')
            return program
        program[program[pc+3]] = opcodes[op](program,pc)
        pc += ADV
    return program

if __name__ == '__main__':
    with open('input.txt') as f:
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
    
    
