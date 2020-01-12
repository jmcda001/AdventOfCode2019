import sys
sys.path.append('../')
from IntcodeComputer.intcode import Program

if __name__ == '__main__':
    fn = 'input.txt'
    with open(fn) as f:
        program = Program([int(i) for i in f.readline().split(',')])
        program.run()
        result = program.instructions
