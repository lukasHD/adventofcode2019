# --- Day 10: Monitoring Station ---

from math import gcd, sqrt, pow, atan, atan2, degrees
from itertools import groupby, cycle

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

def get_station(inStr): 
    for lNr, line in enumerate(inStr.split('\n')):
        for chNr, char in enumerate(line): 
            if char == 'X':
                # is station
                station = (chNr, lNr)
    return station

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

def get_dist(p1, p2):
    # return the direction from p1 to p2 
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]      
    dist = sqrt(pow(dx, 2) + pow(dy, 2))
    return dist

def get_angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # if dx == 0 and dy > 0:
    #     return 9999
    # if dx == 0 and dy < 0:
    #     return 2222
    return (180-degrees(atan2(dx, dy))) % 360


def get_number_visible(base, coordinates):
    directions = set()
    for target in coordinates:
        if (direction := get_direction(base, target)) != None:
            directions.add(direction)
    #print(directions)
    return len(directions)

def get_direction_distance(base, coordinates):
    results = list()
    for target in coordinates:
        if (distance  := get_dist(base, target)) != 0:
            angle      = get_angle(base, target)
            results.append([target, distance, angle])
    return results

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

def shoot(station, asteroids): 
    results = get_direction_distance(station, asteroids)
    results.sort(key= lambda x: (x[2], x[1]))
    # is sorted by angle, then by distance
    print(results)
    old_angle = -1
    counter = 1
    idx = 0 
    shooting_list = []
    while len(results) > 0:
        print("pos {} of {} old_angle = {}".format(idx, len(results), old_angle))
        i = results[idx]
        if i[2] == old_angle:
            print("charge Laser and continue")
            idx += 1 
            if idx > (len(results)-1):
                print("wrap-around inplace")
                # wrap around and forget all charging
                if len(results) > 1:
                    idx = idx % (len(results)-1)
                else:
                    idx = 0
                old_angle = -1
            continue
        print("Shot #{} at {}".format(counter, i[0]))
        shooting_list.append(i[0])
        old_angle = i[2]
        counter += 1
        results.remove(i)
        if len(results) == 0: 
            print("finished")
            break
        if idx > (len(results)-1):
            print("wrap-around iterator")
            # wrap around and forget all charging
            idx = idx % (len(results)-1)
            old_angle = -1
    return shooting_list

def run_small_test2():
    print("small test 2")
    print("************")
    inp = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##"""
    print(inp)
    station = get_station(inp)
    asteroids = get_astroids(inp)
    print(station)
    print(asteroids)

    history_of_targets = shoot(station, asteroids)
    print(history_of_targets)


def runPartTwo():
    inp = read_file2('input')
    station, numVisible = find_best_station(get_astroids(inp))
    asteroids = get_astroids(inp)
    print(station)
    print(asteroids)
    history_of_targets = shoot(station, asteroids)
    print(history_of_targets)
    twohundred = history_of_targets[200-1]
    solution = 100*twohundred[0] + twohundred[1]
    print(solution)

def runPartOne():
    inp = read_file2('input')
    bestLocation, numVisible = find_best_station(get_astroids(inp))
    print(bestLocation)
    print(numVisible)
    return numVisible

if __name__ == '__main__':
    #run_small_test()
    runPartOne()
    #run_small_test2()
    runPartTwo()