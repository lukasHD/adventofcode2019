# https://adventofcode.com/2019/day/1

def calcFuel(mass):
    fuel = int(mass / 3) - 2
    return max(0, fuel)

# def calcFullFuel(mass):
#     fuel = calcFuel(mass)
#     if fuel < 0:
#         fuel = 0
#     print("For mass {} required Fuel is {}".format(mass, fuel))
#     else:
#         additionalFuel = calcFullFuel(fuel)
#         if additionalFuel > 0:
#             fuel = fuel + calcFullFuel(fuel)
#     return fuel

def calcFullFuel(mass):
    '''
    Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.
    '''
    if mass <= 0:
        return 0
    else:
        fuel = calcFuel(mass)
        #print ("Fuel: {}".format(fuel))
        return fuel + calcFullFuel(fuel)

class module:
    def __init__(self, mass=0):
        self.mass = mass

    def requiredFuel(self):
        return int(self.mass / 3) - 2

    def print_fuel(self):
        print("For mass {} required Fuel is {}".format(self.mass, self.requiredFuel()))


def inputToIntList(fname='input'):
    intList = []
    with open(fname, 'r') as f:
        for line in f:
            intList.append(int(line))
    return intList

if __name__ == '__main__':
    modulMasses = inputToIntList()
    # for mass in modulMasses:
    #     #print(mass)
    #     a = module(mass)
    #     a.print_fuel()
    print ("______________")
    fuelList = list(map(lambda x: calcFuel(x), modulMasses))
    fullFuelList = list(map(lambda x: calcFullFuel(x), modulMasses))
    #print(fuelList)
    print(sum(fuelList)) #should return 3299598
    print(sum(fullFuelList)) #should return 4946546
    #unittest.main()