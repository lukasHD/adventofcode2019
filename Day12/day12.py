# --- Day 12: The N-Body Problem ---

# Io, Europa, Ganymede, and Callisto

from itertools import combinations

class Moon():

    def __init__(self, _x=0, _y=0, _z=0, _vx=0, _vy=0, _vz=0, _name='None'):
        self.x  = _x
        self.y  = _y
        self.z  = _z
        self.vx = _vx
        self.vy = _vy
        self.vz = _vz
        self.name = _name

    def print(self):
        print("{:>10}: pos=<x={:4d}, y={:4d}, z={:4d}>, vel=<x={:4d}, y={:4d}, z={:4d}>".format(self.name, self.x, self.y, self.z, self.vx, self.vy, self.vz))

    def propagate(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.z = self.z + self.vz

    def getPotEnergy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z))
    
    def getKinEnergy(self):
        return (abs(self.vx) + abs(self.vy) + abs(self.vz))
    
    def getTotEnergy(self):
        return (self.getKinEnergy() * self.getPotEnergy())

class System():

    def __init__(self):
        self.MoonList =[]
        self.steps = 0

    def addMoon(self, _moon):
        self.MoonList.append(_moon)

    def gravity(self, moon1, moon2):
        # X-Axis
        if moon1.x < moon2.x:
            moon1.vx = moon1.vx + 1
            moon2.vx = moon2.vx - 1
        elif moon1.x > moon2.x:
            moon1.vx = moon1.vx - 1
            moon2.vx = moon2.vx + 1
        # Y-Axis
        if moon1.y < moon2.y:
            moon1.vy = moon1.vy + 1
            moon2.vy = moon2.vy - 1
        elif moon1.y > moon2.y:
            moon1.vy = moon1.vy - 1
            moon2.vy = moon2.vy + 1
        # Z-Axis
        if moon1.z < moon2.z:
            moon1.vz = moon1.vz + 1
            moon2.vz = moon2.vz - 1
        elif moon1.z > moon2.z:
            moon1.vz = moon1.vz - 1
            moon2.vz = moon2.vz + 1
        # finished this pair
        return moon1, moon2

    def getTotEnergy(self):
        tot = 0
        for moon in self.MoonList:
            tot += moon.getTotEnergy()
        return tot

    def step(self):
        self.steps += 1
        print("Step {}".format(self.steps))
        # calc gravity for each pair in moons
        for moonID in combinations(range(len(self.MoonList)),  r=2):
            #print("Gravity of {:>10} and {:>10}".format(moons[0].name, moons[1].name))
            self.MoonList[moonID[0]], self.MoonList[moonID[1]] = self.gravity(self.MoonList[moonID[0]], self.MoonList[moonID[1]])
        # propagate all moons
        for moon in self.MoonList:
            moon.propagate()

    def print(self):
        for moon in self.MoonList:
            moon.print()


def run_small_test():
    print("small Test 1")
    print("############")
    # <x=-8, y=-10, z=0>
    # <x=5, y=5, z=10>
    # <x=2, y=-7, z=3>
    # <x=9, y=-8, z=-3>
    system = System()
    system.addMoon(Moon(_name='Io'      , _x=-8, _y=-10, _z= 0 ))
    system.addMoon(Moon(_name='Europa'  , _x= 5, _y=  5, _z=10 ))
    system.addMoon(Moon(_name='Ganymede', _x= 2, _y= -7, _z= 3 ))
    system.addMoon(Moon(_name='Callisto', _x= 9, _y= -8, _z=-3 ))
    for _ in range(100):
        system.step()
        system.print()
    print(system.getTotEnergy())

def runPartOne():
    print("run Part One")
    print("############")
    system = System()
    system.addMoon(Moon(_name='Io'      , _x=1 , _y=3  , _z=-11 ))
    system.addMoon(Moon(_name='Europa'  , _x=17, _y=-10, _z=-8  ))
    system.addMoon(Moon(_name='Ganymede', _x=-1, _y=-15, _z=2   ))
    system.addMoon(Moon(_name='Callisto', _x=12, _y=-4 , _z=-4  ))
    for _ in range(1000):
        system.step()
    system.print()
    print(system.getTotEnergy())

def run_small_test2():
    print("small Test 2")
    print("############")

def runPartTwo():
    print("run Part Two")
    print("############")


if __name__ == '__main__':
    run_small_test()
    runPartOne()
    run_small_test2()
    runPartTwo()