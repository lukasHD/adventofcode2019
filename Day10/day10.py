# --- Day 10: Monitoring Station ---

from math import gcd

def read_file(fname):
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content]

def read_file2(fname):
    with open(fname) as f:
        content = f.read()
    return content

inpA = """.#..#
.....
#####
....#
...##"""

def get_astroids(inStr): 
    coordinates = []
    for lNr, line in enumerate(inStr.split('\n')):
        for chNr, char in enumerate(line): 
            if char == '#':
                # is astroid
                coordinates.append((chNr, lNr))
    #print(coordinates)
    return coordinates

def get_direction(p1, p2):
    # return the direction from p1 to p2 
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]      
    if (divisor := gcd(dx, dy)) != 0:
        dx /= divisor
        dy /= divisor
    else:
        return None
    return (int(dx), int(dy))

def get_number_visible(base, coordinates):
    directions = set()
    for target in coordinates:
        if (direction := get_direction(base, target)) != None:
            directions.add(direction)
    #print(directions)
    return len(directions)

def find_best_station(coordinates):
    scan = []
    for astroid in coordinates:
        scan.append([astroid, get_number_visible(astroid, coordinates)])
    #print("SCAN")
    #print(scan)
    bestLocation, numVisible = max(scan, key=lambda x: x[1])
    #print(bestLocation)
    #print(numVisible)
    return  bestLocation, numVisible

def run_small_test():
    print("small test")
    coordinates = get_astroids(inpA)
    # print(get_direction((0,0),(1,2)))
    # print(get_direction((0,0),(2,4)))
    # print(get_direction((1,2),(0,0)))
    # print(get_number_visible((0,1), coordinates))
    find_best_station(coordinates)

    return 0

def runPartOne():
    inp = read_file2('input')
    bestLocation, numVisible = find_best_station(get_astroids(inp))
    print(bestLocation)
    print(numVisible)
    return numVisible

if __name__ == '__main__':
    runPartOne()
    #run_small_test()
    #runPartTwo()