from typing import List,Dict
from collections import defaultdict
from heapq import heappush, heappop

# Create an adjacency list representation of an undirected graph
def parseOrbits(orbits: List[str])->Dict[str,List[str]]:
    g:Dict[str,List[str]] =defaultdict(list)
    for orbit in orbits:
        orbitsymbolindex = orbit.find(')')
        center = orbit[0:orbitsymbolindex]
        satellite = orbit[orbitsymbolindex+1:]
        g[center].append(satellite)
        g[satellite].append(center)
    return g

# Calculate the total orbits (direct + indirect) in the system
def totalOrbits(g: Dict[str,List[str]],planet: str ='COM')->int:
    return orbitDistance(g,planet,'')

class BFS_Node:
    planet: str
    distance: int
    previous: str

    def __init__(self,p):
        self.planet = p
        self.distance = None
        self.previous = None

    def __lt__(self, other):
        if self.distance is None:
            return False
        if other.distance is None:
            return True
        return self.distance < other.distance

    def __str__(self):
        return f'{self.planet} ({self.distance})'

def traceOrbit(bfs: Dict[str,BFS_Node],endPlanet: str)->List[str]:
    trace:List[str] = []
    current = bfs[endPlanet]
    if not current:
        return trace
    while current.previous:
        trace.append(str(current))
        current = bfs[current.previous]
    return trace 

def orbitDistance(g: Dict[str,List[str]],startPlanet: str,endPlanet: str)->int:
    bfs = {}
    for p in g:
        bfs[p] = BFS_Node(p)
    heap:List[BFS_Node] = []
    visited = set()
    totalOrbits = 0
    bfs[startPlanet].distance = -1
    heappush(heap,bfs[startPlanet])
    while heap:
        current = heappop(heap)
        if current.planet == endPlanet:
            return bfs[endPlanet].distance - 1 
        visited.add(current.planet)
        totalOrbits += current.distance + 1
        for nextPlanet in [p for p in g[current.planet] if p not in visited]:
            bfs[nextPlanet].distance = current.distance+1
            bfs[nextPlanet].previous = current.planet
            heappush(heap,bfs[nextPlanet])
    return totalOrbits


if __name__ == '__main__':
    with open('input.txt') as f:
        g = parseOrbits([orbit.strip() for orbit in f.readlines()])
        print(orbitDistance(g,'YOU','SAN'))

def test_orbitDistance():
    testInput = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN']
    startPlanet,endPlanet = 'YOU','SAN'
    orbits = orbitDistance(parseOrbits(testInput),startPlanet,endPlanet)
    assert orbits == 4

def test_totalOrbits():
    testInput = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L',]
    orbits = totalOrbits(parseOrbits(testInput))
    assert orbits == 42

def test_BFS_Node():
    nodeName = 'test'
    testNode = BFS_Node(nodeName)
    assert testNode.planet == nodeName
    assert testNode.distance is None
    assert testNode.previous is None

    nodeName = 'distanceNotNone'
    testNodeNotNone = BFS_Node(nodeName)
    testNodeNotNone.distance = 2
    assert (testNodeNotNone < testNode) is True
    assert (testNodeNotNone > testNode) is False

    testNode.distance = 3
    assert (testNodeNotNone < testNode) is True
    assert (testNode < testNodeNotNone) is False

