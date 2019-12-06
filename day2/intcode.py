from typing import List

opcodes = {1: (lambda p,i: p[p[i+1]]+p[p[i+2]]),
    2: (lambda p,i: p[p[i+1]]*p[p[i+2]]),
}

def runProgram(program: List[int])->List[int]:
    i = 0
    while i < len(program) and program[i] != 99:
        op = program[i]
        if op not in opcodes:
            print(f'Error: Encountered unknown opcode {op} at index {i}')
            return program
        program[program[i+3]] = opcodes[op](program,i)
        i += 4
    return program

def test():
    # Test 1
    testInput = [1,0,0,0,99]
    expected = [2,0,0,0,99]
    print(f'Running program on {testInput}...',end='')
    output = runProgram(testInput)
    if output != expected:
        print(f'Received {output} but expected {expected}')
    else:
        print('Passed')
    
    # Test 2
    testInput = [2,3,0,3,99]
    expected = [2,3,0,6,99]
    print(f'Running program on {testInput}...',end='')
    output = runProgram(testInput)
    if output != expected:
        print(f'Received {output} but expected {expected}')
    else:
        print('Passed')
    
    # Test 3
    testInput = [2,4,4,5,99,0]
    expected = [2,4,4,5,99,9801]
    print(f'Running program on {testInput}...',end='')
    output = runProgram(testInput)
    if output != expected:
        print(f'Received {output} but expected {expected}')
    else:
        print('Passed')
    
    # Test 4
    testInput = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    print(f'Running program on {testInput}...',end='')
    output = runProgram(testInput)
    if output != expected:
        print(f'Received {output} but expected {expected}')
    else:
        print('Passed')
    
if __name__ == '__main__':
    test()
    with open('input.txt') as f:
        program = [int(i) for i in f.readline().split(',')]
        program[1] = 12
        program[2] = 2
        output = runProgram(program)
        print(f'Output at index 0 after running modified program is {output[0]}')
