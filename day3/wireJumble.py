import sys
import copy
from typing import List, Generator
from collections import namedtuple,defaultdict

Point=namedtuple('Point','x y')
origin = Point(x=1,y=1)

def manhattanDistance(a: Point,b: Point)->int:
    distance = abs(a.x - b.x) + abs(a.y - b.y)
    return distance

def manhattanDistance_test()->bool:
    suite = 'Manhattan Distance'
    passed = True
    testNum = 1
    print(f'{suite}: Test #{testNum}',end='...')
    testInput = [Point(x=1,y=1),Point(x=4,y=4),]
    expected = 6
    result = manhattanDistance(testInput[0],testInput[1])
    if result != expected:
        print(f'Failed. Expected {expected} but result is {result}')
        passed = False
    else:
        print('Passed')
    return passed

delta={'U': lambda p,amnt: Point(p.x,p.y+amnt),
    'R': lambda p,amnt: Point(p.x+amnt,p.y),
    'D': lambda p,amnt: Point(p.x,p.y-amnt),
    'L': lambda p,amnt: Point(p.x-amnt,p.y)}

def expandPoints(wire: List[str])->List[Point]:
    oldPoint = origin
    allPoints = []
    steps = 0
    for dirChange in wire:
        newPoints = [(delta[dirChange[0]](oldPoint,i+1),steps+i) for i in range(1,int(dirChange[1:]))]
        steps += int(dirChange[1:])
        oldPoint = newPoints[-1][0]
        allPoints.extend(newPoints)
    return allPoints

def expandPoints_gen(wire: List[str]) -> Generator[Point,None,None]:
        oldPoint = origin
        steps = 0
        for dirChange in wire:
            for amnt in range(0,int(dirChange[1:])):
                steps += 1
                oldPoint = delta[dirChange[0]](oldPoint,1)
                yield oldPoint,steps
            yield 'changeDir',steps
        return 'Done',steps

def expandPoints_test()->bool:
    suite = 'Expand Points'
    passed = True
    testNum = 1
    print(f'{suite}: Test #{testNum}',end='...')
    testInput = ['R2','U3','L2','D3']
    expected = origin
    result = expandPoints(testInput)
    if result[-1][0] != expected: # Check if this goes full circle
        print(f'Failed. Expected {expected} but result is {result}')
        passed = False
    else:
        print('Passed')
    return passed
    
def wireJumble_hash(wireA: List[str],wireB: List[str])->(int,Point):
    currentPoint = origin
    xHash = defaultdict(list)
    yHash = defaultdict(list)
    steps = 0
    for segment in wireA:
        direction = segment[0]
        amount = int(segment[1:])
        nextPoint = delta[direction](currentPoint,amount)
        if direction in ['U','D']:
            xHash[currentPoint.x].append((currentPoint.y,nextPoint.y,steps))
        else:
            yHash[currentPoint.y].append((currentPoint.x,nextPoint.x,steps))
        steps += amount
        currentPoint = nextPoint
    possibleIntersection = None
    minDistance = None
    changes = 0
    possibleSolutions = []
    for p,steps in expandPoints_gen(wireB):
        if p == 'changeDir':
            changes += 1
            continue
        possibleIntersection = None
        if p.x in xHash:
            for yPair in xHash[p.x]:
                if min(yPair[0:2]) < p.y and p.y < max(yPair[0:2]):
                    possibleIntersection = p
                    possibleSteps = yPair[2] + abs(p.y - yPair[0])
                    break
        if p.y in yHash:
            for xPair in yHash[p.y]:
                if min(xPair[0:2]) < p.x and p.x < max(xPair[0:2]): 
                    possibleIntersection = p
                    possibleSteps = xPair[2] + abs(p.x - xPair[0])
                    break
        if possibleIntersection is None:
            continue
        smallestMH = lambda p: manhattanDistance(origin,p) < minDistance #part 1
        smallestSteps = lambda p: possibleSteps + steps < minDistance #part 2
        closest = smallestSteps
        if  minDistance is None or closest(possibleIntersection):
            minDistance = possibleSteps + steps
            solution = possibleIntersection

    return minDistance,solution


def wireJumble(wireA: List[str],wireB: List[str])->(int,Point):
    allA = expandPoints(wireA)
    allB = expandPoints(wireB)
    intersections = set(allA[1:]).intersection(set(allB[1:]))
    minDistance = None
    for intersection in intersections:
        if minDistance is None or manhattanDistance(origin,intersection) < minDistance:
            minDistance = manhattanDistance(origin,intersection)
            solution = intersection
    return minDistance,solution

def wireJumble_test()->bool:
    fn = wireJumble_hash
    part1 = False
    suite = 'Wire Jumble'
    passed = True
    testNum = 1
    print(f'{suite}: Test #{testNum}',end='...')
    testInput = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
        ['U62','R66','U55','R34','D71','R55','D58','R83']]
    expected = 159 if part1 else 610
    result,point = fn(testInput[0],testInput[1])
    if result != expected:
        print(f'Failed. Expected {expected} but result is {result}')
        print(f'\t{point} is {result} steps from {origin}')
        passed = False
    else:
        print('Passed')

    testNum += 1
    print(f'{suite}: Test #{testNum}',end='...')
    testInput = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
        ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]
    expected = 135 if part1 else 410
    result,point = fn(testInput[0],testInput[1])
    if result != expected:
        print(f'Failed. Expected {expected} but result is {result}')
        print(f'\t{point} is {result} steps from {origin}')
        passed = False
    else:
        print('Passed')

    testNum += 1
    print(f'{suite}: Test #{testNum}',end='...')
    testInput = [['R8','U5','L5','D3'],
        ['U7','R6','D4','L4']]
    expected = 6 if part1 else 30
    result,point = fn(testInput[0],testInput[1])
    if result != expected:
        print(f'Failed. Expected {expected} but result is {result}')
        print(f'\t{point} is {result} steps from {origin}')
        passed = False
    else:
        print('Passed')

    return passed

def readFile(fn:str)->(List[str],List[str]):
    with open(fn) as f:
        wireA = f.readline().split(',')
        wireB = f.readline().split(',')
        return wireA,wireB
    return [],[]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        fn = 'input.txt'
    else:
        fn = sys.argv[1]
    if not manhattanDistance_test():
        print('manhattanDistance tests failed. Exiting...')
        exit()
    if not expandPoints_test():
        print('expandPoints tests failed. Exiting...')
        exit()
    if not wireJumble_test():
        print('wireJumble tests failed. Exiting...')
        exit()

    wireA,wireB =  readFile(fn)
    distance,point = wireJumble_hash(wireA,wireB)
    print(f'Manhattan distance = {distance}')

