from typing import Optional,List,Dict,Tuple
from pprint import pprint
from collections import namedtuple,defaultdict
import math
import itertools

EMPTY='.'
ASTEROID='#'

Asteroid = namedtuple('Asteroid','X Y')
Slope = namedtuple('Slope','rise run')

def part1(filename:str)->Tuple[Optional[Tuple[int,int]],int]:
    with open(filename,'r') as f:
        asteroids = findAsteroidVisibility(f)
        best = findBestAsteroid(asteroids)
    return best,asteroids[best]

def part2(filename):
    with open(filename,'r') as f:
        asteroids = findAsteroidVisibility(f)
        best = findBestAsteroid(asteroids)
        slopes = findSlopes(asteroids,best)
        hit1: Dict[float,List[Tuple[Asteroid,int]]] = {}
        hit2: Dict[float,List[Tuple[Asteroid,int]]] = {}
        hit3: Dict[float,List[Tuple[Asteroid,int]]] = {}
        hit4: Dict[float,List[Tuple[Asteroid,int]]] = {}
        for slope in slopes:
            if slope.rise <= 0 and slope.run >= 0:
                hit1[math.atan2(slope.rise,slope.run)] = slopes[slope]
            elif slope.rise > 0 and slope.run > 0:
                hit2[math.atan2(slope.rise,slope.run)] = slopes[slope]
            elif slope.rise >= 0 and slope.run <= 0:
                hit3[math.atan2(slope.rise,slope.run)] = slopes[slope]
            elif slope.rise < 0 and slope.run < 0:
                hit4[math.atan2(slope.rise,slope.run)] = slopes[slope]
        hitOrder = [hit1,hit2,hit3,hit4]
        BetAsteroid = 200
        lastAsteroid = None
        hits = 0
        while lastAsteroid == None:
            for j,hitDict in enumerate(hitOrder):
                for i,h in enumerate(sorted(list(dict.keys(hitDict)))):
                    if len(hitDict[h]) == 0: # Skip this if all asteroids on this trajectory have been zapped
                        continue
                    # TODO: Remove hitDict[h] first element
                    hits += 1
                    if hits == BetAsteroid:
                        lastAsteroid = hitDict[h][0][0]
                        break
    return lastAsteroid.X * 100 + lastAsteroid.Y

def findBestAsteroid(asteroids: Dict[Asteroid,int])->Optional[Asteroid]:
    bestAsteroid,maxVisible = None,0
    for asteroid in asteroids:
        if asteroids[asteroid] > maxVisible:
            bestAsteroid,maxVisible = asteroid,asteroids[asteroid]
    return bestAsteroid

def findAsteroidVisibility(f)->Dict[Asteroid,int]:
    space = []
    asteroids: Dict[Asteroid,int] = {}
    for line in f.readlines():
        space.append(line.strip())
    for j,row in enumerate(space):
        for i,loc in enumerate(row):
            if loc == '#':
                newAsteroid = Asteroid(i,j)
                updateVisible(asteroids,newAsteroid)
    return asteroids

def findSlopes(asteroids: Dict[Asteroid,int],newAsteroid: Asteroid)->Dict[Slope,List[Tuple[Asteroid,int]]]:
    slopes: Dict[Slope,List[Tuple[Asteroid,int]]] = defaultdict(list)
    for other in asteroids:
        if other == newAsteroid:
            continue
        rise = other.Y - newAsteroid.Y
        run = other.X - newAsteroid.X
        gcd = math.gcd(rise,run)
        slope = Slope(rise/gcd,run/gcd)
        slopes[slope].append((other,gcd))
    return slopes

def updateVisible(asteroids: Dict[Asteroid,int],newAsteroid: Asteroid)->None:
    slopes = findSlopes(asteroids,newAsteroid)
    # Update the visibility of all of them
    for s in slopes:
        neg = False
        pos = False
        for entry in sorted(slopes[s],key=lambda entry: abs(entry[1])):
            if not neg and entry[1] < 0:
                neg = True
                asteroids[entry[0]] += 1
            if not pos and entry[1] > 0:
                pos = True
                asteroids[entry[0]] += 1
    asteroids[newAsteroid] = len(slopes)

def test_part1():
    day='day10_MonitoringStation/'
    filename = 'test33.txt'
    assert part1(day+filename) == ((5,8),33)
    filename = 'test35.txt'
    assert part1(day+filename) == ((1,2),35)
    filename = 'test41.txt'
    assert part1(day+filename) == ((6,3),41)
    filename = 'test210.txt'
    assert part1(day+filename) == ((11,13),210)

