from typing import NamedTuple, List
import inspect 

class Instruction():
    opcode: str
    mode1: bool
    mode2: bool
    mode3: bool
    def __init__(self,opcode,modes):
        self.opcode = opcode
        self.mode1,self.mode2,self.mode2 = modes

class jumpIfTrue(Instruction):
    def __init__(self,modes):
        Instruction.__init__(self,'05',modes)
        condition = (lambda p,pc: p[pc+1]) if self.mode1 else (lambda p,pc: p[p[pc+1]])
        jumpAddress = (lambda p,pc: p[pc+2]) if self.mode2 else (lambda p,pc: p[p[pc+2]])
        self.execute = (lambda p,pc: (jumpAddress(p,pc) - pc if condition(p,pc) == 1 else 3))
j = jumpIfTrue((True,True,False))
testInput = [5,0,1]
pc = 0
breakpoint()
j.execute(testInput,pc)
print(inspect.getsource(j.execute))
print(inspect.getsource(j.execute))
        
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

ISA = {1: add, 
     2: multiply, 
    3: takeInput, 
    4: sendOutput, 
    5: jumpIfTrue,
    6: jumpIfFalse,
    7: lessThan,
    8: equals,
}

import pytest

runInstruction = lambda op,p,pc,i: op(p,pc,i)
def test_correctOp():
    testInput = Instruction('01','0','0','0')
    op = ISA[int(testInput.opcode)]
    assert op is add

    testInput = Instruction('02','0','0','0')
    op = ISA[int(testInput.opcode)]
    assert op is multiply

    testInput = Instruction('03','0','0','0')
    op = ISA[int(testInput.opcode)]
    assert op is takeInput

    testInput = Instruction('04','0','0','0')
    op = ISA[int(testInput.opcode)]
    assert op is sendOutput

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

def test_jumpIfFalse():
    testInput = [6,1,0]
    pc = 0
    pc = pc + jumpIfFalse(testInput,pc,Instruction('06',True,False,False))
    assert pc == 3

    testInput = [6,0,1]
    pc = 0
    pc = pc + jumpIfFalse(testInput,pc,Instruction('06',True,False,False))
    assert pc == 0

def test_jumpIfTrue():
    testInput = [5,2,0]
    pc = 0
    pc = pc + jumpIfTrue(testInput,pc,Instruction('05',False,False,False))
    assert pc == 3

    testInput = [5,2,1]
    pc = 0
    pc = pc + jumpIfTrue(testInput,pc,Instruction('05',False,False,False))
    assert pc == 2

    testInput = [5,2,1]
    pc = 0
    pc = pc + jumpIfTrue(testInput,pc,Instruction('05',False,True,False))
    assert pc == 1

    testInput = [5,2,0]
    pc = 0
    pc = pc + jumpIfTrue(testInput,pc,Instruction('05',True,False,False))
    assert pc == 3

    testInput = [5,2,1]
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
