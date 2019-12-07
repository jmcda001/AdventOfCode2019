from typing import List, NamedTuple
from collections import namedtuple

class Instruction(NamedTuple):
    opcode: str
    mode1: bool
    mode2: bool
    mode3: bool

runInstruction = lambda op,p,pc,i: op(p,pc,i)
def add(program: List[int],pc: int,instruction: Instruction)->int:
    try:
        a = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
        b = program[program[pc+2]] if not instruction.mode2 else program[pc+2]
        program[program[pc+3]] = int(a) + int(b)
    except IndexError as e:
        print(f'Caught {e} on instruction: {instruction} in program: {program[pc:pc+4]}')
    return 4

def multiply(program: List[int],pc: int,instruction: Instruction)->int:
    try:
        a = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
        b = program[program[pc+2]] if not instruction.mode2 else program[pc+2]
        program[program[pc+3]] = int(a) * int(b)
    except IndexError as e:
        print(f'Caught {e} on instruction: {instruction} in program: {program[pc:pc+4]}')
    return 4

def takeInput(program: List[int],pc: int,instruction: Instruction)->int:
    program[program[pc+1]] = input()
    return 2

def sendOutput(program: List[int],pc: int,instruction: Instruction)->int:
    print(program[program[pc+1]])
    return 2

opcodes = {1: add, 2: multiply, 3: takeInput, 4: sendOutput}

def instructionDecode(opcode: int)->Instruction:
    opcodeList = [i for i in str(opcode)]
    extension = []
    if len(opcodeList) < 5:
        extension = ['0']*(5-len(opcodeList))
    opcodeList = extension+opcodeList
    opcodeValue = ''.join(opcodeList[3:])
    modes = bool(int(opcodeList[2])),bool(int(opcodeList[1])),bool(int(opcodeList[0]))
    instruction = Instruction(opcodeValue,*modes)
    return instruction

def runProgram(program: List[int])->List[int]:
    pc = 0
    while pc < len(program) and program[pc] != 99:
        instruction = instructionDecode(program[pc])
        if int(instruction.opcode) not in opcodes:
            print(f'Error: Encountered unknown opcode {instruction.opcode} at index {pc}')
            return program
        advance = opcodes[int(instruction.opcode)](program,pc,instruction)
        pc += advance
    return program

if __name__ == '__main__':
    with open('input.txt') as f:
        program = [int(i) for i in f.readline().split(',')]
        runProgram(program)

import pytest
def test_correctOp():
    testInput = Instruction('01','0','0','0')
    op = opcodes[int(testInput.opcode)]
    assert op is add

    testInput = Instruction('02','0','0','0')
    op = opcodes[int(testInput.opcode)]
    assert op is multiply

    testInput = Instruction('03','0','0','0')
    op = opcodes[int(testInput.opcode)]
    assert op is takeInput

    testInput = Instruction('04','0','0','0')
    op = opcodes[int(testInput.opcode)]
    assert op is sendOutput

def test_runProgram():
    # Test 1
    testInput = [1,0,0,0,99]
    expected = [2,0,0,0,99]
    output = runProgram(testInput)
    assert output == expected
    
    # Test 2
    testInput = [2,3,0,3,99]
    expected = [2,3,0,6,99]
    output = runProgram(testInput)
    assert output == expected
    
    # Test 3
    testInput = [2,4,4,5,99,0]
    expected = [2,4,4,5,99,9801]
    output = runProgram(testInput)
    assert output == expected
    
    # Test 4
    testInput = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    output = runProgram(testInput)
    assert output == expected

def test_instructionDecode():
    opcode = 1002
    expected = Instruction('02',False,True,False)
    assert instructionDecode(opcode) == expected
    opcode = 11102
    expected = Instruction('02',True,True,True)
    assert instructionDecode(opcode) == expected
    opcode = 1
    expected = Instruction('01',False,False,False)
    assert instructionDecode(opcode) == expected
    opcode = 101
    expected = Instruction('01',True,False,False)
    assert instructionDecode(opcode) == expected

def test_add():
    testProgram = [1101,100,-1,4,0]
    testInstruction = Instruction(1,1,1,0)
    pc = 0
    expected = [1101,100,-1,4,99]
    runInstruction(add,testProgram,pc,testInstruction)
    assert testProgram == expected

    testProgram = [1101,100,-1,4,0]
    testInstruction = Instruction('1','1','1','0')
    pc = 0
    expected = [1101,100,-1,4,99]
    runInstruction(add,testProgram,pc,testInstruction)
    assert testProgram == expected

def test_add2():
    testProgram = [1,0,0,0,99]
    testInstruction = Instruction(1,0,0,0)
    pc = 0
    expected = [2,0,0,0,99]
    runInstruction(add,testProgram,pc,testInstruction)
    assert testProgram == expected

def test_multiply():
    testProgram = [1002,4,3,4,33]
    testInstruction = Instruction(2,0,1,0)
    pc = 0
    expected = [1002,4,3,4,99]
    runInstruction(multiply,testProgram,pc,testInstruction)
    assert testProgram == expected

@pytest.mark.skip(reason='No way to mock input currently')
def test_takeInput(): #
    testProgram = [3,0]
    testInstruction = Instruction(3,0,0,0)
    pc = 0
    inputValue = 5
    expected = [inputValue,0]
    with mock.patch.object(__builtins__,'input',lambda: str(inputValue)):
        runInstruction(takeInput,testProgram,pc,testInstruction)
    assert testProgram == expected

def test_sendOutput(capfd):
    outputValue = 5
    testProgram = [4,2,outputValue]
    testInstruction = Instruction(4,0,0,0)
    pc = 0
    runInstruction(sendOutput,testProgram,pc,testInstruction)
    captured = capfd.readouterr()
    assert captured.out.strip() == str(outputValue)

