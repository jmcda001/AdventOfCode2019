import sys
from typing import List, NamedTuple
from collections import namedtuple

class Instruction(NamedTuple):
    opcode: str
    mode1: bool
    mode2: bool
    mode3: bool

#TODO: Not working
parameter1 = lambda p,pc,mode: p[p[pc+1]] if not mode else p[pc+1]
parameter2 = lambda p,pc,mode: p[p[pc+1]] if not mode else p[pc+1]
def jumpIfTrue(program: List[int], pc: int, instruction: Instruction)->int:
    condition = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
    jumpAddress = program[program[pc+2]] if not instruction.mode2 else program[pc+2]
    if condition == 1:
        return jumpAddress - pc # Advance to program[pc+2]
    return 3 # Advance to end of instruction

def jumpIfFalse(program: List[int], pc: int, instruction: Instruction)->int:
    condition = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
    jumpAddress = program[program[pc+2]] if not instruction.mode2 else program[pc+2]
    if condition == 0:
        return jumpAddress - pc # Advance to program[pc+2]
    return 3 # Advance to end of instruction

def lessThan(program: List[int], pc: int, instruction: Instruction)->int:
    try:
        a = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
        b = program[program[pc+2]] if not instruction.mode2 else program[pc+2]
        program[program[pc+3]] = int(a < b)
    except (IndexError,TypeError) as e:
        print(f'Caught {e} on instruction: {instruction} in program: {program[pc:pc+4]}')
    return 4

def equals(program: List[int], pc: int, instruction: Instruction)->int:
    try:
        a = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
        b = program[program[pc+2]] if not instruction.mode2 else program[pc+2]
        program[program[pc+3]] = int(a == b)
    except IndexError as e:
        print(f'Caught {e} on instruction: {instruction} in program: {program[pc:pc+4]}')
    return 4

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
    program[program[pc+1]] = int(input())
    return 2

def sendOutput(program: List[int],pc: int,instruction: Instruction)->int:
    try:
        a = program[program[pc+1]] if not instruction.mode1 else program[pc+1]
        print(a)
    except IndexError as e:
        print(f'Caught {e} on instruction: {instruction} in program: {program[pc:pc+4]}')
    return 2

opcodes = {1: add, 
    2: multiply, 
    3: takeInput, 
    4: sendOutput, 
    5: jumpIfTrue,
    6: jumpIfFalse,
    7: lessThan,
    8: equals,
}

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
            print(f'Error: Encountered unknown opcode {instruction.opcode} at index {pc} in {program}')
            return program
        advance = opcodes[int(instruction.opcode)](program,pc,instruction)
        pc += advance
    return program

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = 'input.txt'
    with open(fn) as f:
        program = [int(i) for i in f.readline().split(',')]
        result = runProgram(program)

import pytest

runInstruction = lambda op,p,pc,i: op(p,pc,i)
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
def testrunProgram(capfd):
    testInput = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    runProgram(testInput)
    captured = capfd.readouterr()
    assert captured.out.strip() == 1

    testInput = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    runProgram(testInput)
    assert captured.out.strip() == 0

    testInput = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,
        46,1101,1000,1,20,4,20,1105,1,46,98,99]
    runProgram(testInput)
    assert captured.out.strip() == 0

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

def test_jumpIfFalse():
    testInput = [6,1,0]
    pc = 0
    pc = pc + jumpIfFalse(testInput,pc,Instruction('06',True,False,False))
    assert pc == 3

    testInput = [6,0,0]
    pc = 0
    pc = pc + jumpIfFalse(testInput,pc,Instruction('06',True,False,False))
    assert pc == 0

def test_jumpIfTrue():
    testInput = [5,1,0]
    pc = 0
    pc = pc + jumpIfTrue(testInput,pc,Instruction('05',True,False,False))
    assert pc == 0

    testInput = [5,0,0]
    pc = 0
    pc = pc + jumpIfTrue(testInput,pc,Instruction('05',True,False,False))
    assert pc == 3

def test_lessThan():
    testInput = [7,1,2,3]
    pc = 0
    lessThan(testInput,pc,Instruction('07',True,True,False))
    assert testInput[-1] == 1

    testInput = [7,2,1,3]
    pc = 0
    lessThan(testInput,pc,Instruction('07',True,True,False))
    assert testInput[-1] == 0

    testInput = [7,4,5,5,1,2]
    pc = 0
    lessThan(testInput,pc,Instruction('07',False,False,False))
    assert testInput[-1] == 1 

    testInput = [7,4,5,5,2,1]
    pc = 0
    lessThan(testInput,pc,Instruction('07',False,False,False))
    assert testInput[-1] == 0

def test_equals():
    testInput = [8,5,5,3]
    pc = 0
    equals(testInput,pc,Instruction('08',True,True,False))
    assert testInput[-1] == 1

    testInput = [8,5,4,3]
    pc = 0
    equals(testInput,pc,Instruction('08',True,True,False))
    assert testInput[-1] == 0
