import sys
import pytest
from IntcodeComputer.Instructions import Instruction, ISA
from typing import List, NamedTuple, Dict, Callable
from collections import namedtuple


_TERMINATE = 99
class Program:
    instructions: List[int]
    isa: Dict[str, Callable[[List[int],int,Instruction],int]]
    pc: int

    def __init__(self,i: List[int]):
        self.instructions = i

    def instructionDecode(self,opcode: int)->Instruction:
        opcodeList = [i for i in str(opcode)]
        extension: List[str] = []
        if len(opcodeList) < 5:
            extension = ['0']*(5-len(opcodeList))
        opcodeList = extension+opcodeList
        opcodeValue = ''.join(opcodeList[3:])
        modes = bool(int(opcodeList[2])),bool(int(opcodeList[1])),bool(int(opcodeList[0]))
        return Instruction(opcodeValue,modes)

    def run(self):
        self.pc = 0
        while self.pc < len(self.instructions) and self.instructions[self.pc] != _TERMINATE:
            instruction = self.instructionDecode(self.instructions[self.pc])
            if int(instruction.opcode) not in ISA:
                print(f'Error: Encountered unknown opcode {instruction.opcode} at index {self.pc} in {self.program}')
                return 
            advance = ISA[int(instruction.opcode)](self.instructions,self.pc,instruction)
            self.pc += advance

def test_Program():
    # Test 1
    testInput = [1,0,0,0,99]
    expected = [2,0,0,0,99]
    testProgram = Program(testInput)
    testProgram.run()
    assert testProgram.instructions == expected
    
    # Test 2
    testInput = [2,3,0,3,99]
    expected = [2,3,0,6,99]
    testProgram = Program(testInput)
    testProgram.run()
    output = testProgram.instructions
    assert output == expected
    
    # Test 3
    testInput = [2,4,4,5,99,0]
    expected = [2,4,4,5,99,9801]
    testProgram = Program(testInput)
    testProgram.run()
    output = testProgram.instructions
    assert output == expected
    
    # Test 4
    testInput = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    testProgram = Program(testInput)
    testProgram.run()
    output = testProgram.instructions
    assert output == expected

def test_instructionDecode():
    opcode = 1002
    expected = Instruction('02',False,True,False)
    assert Program.instructionDecode(None,opcode) == expected
    opcode = 11102
    expected = Instruction('02',True,True,True)
    assert Program.instructionDecode(None,opcode) == expected
    opcode = 1
    expected = Instruction('01',False,False,False)
    assert Program.instructionDecode(None,opcode) == expected
    opcode = 101
    expected = Instruction('01',True,False,False)
    assert Program.instructionDecode(None,opcode) == expected

@pytest.mark.skip(reason='No way to mock input currently')
def test_runProgram(capfd):
    testInput = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    testProgram = Program(testInput)
    testProgram.run()
    captured = capfd.readouterr()
    assert captured.out.strip() == 1

    testInput = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    testProgram = Program(testInput)
    testProgram.run()
    assert captured.out.strip() == 0

    testInput = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,
        46,1101,1000,1,20,4,20,1105,1,46,98,99]
    testProgram = Program(testInput)
    testProgram.run()
    assert captured.out.strip() == 0

