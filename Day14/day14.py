# --- Day 14: Space Stoichiometry ---

from collections import defaultdict

class Resources:

    def __init__(self):
        self.reactions = defaultdict(int)
    
    def add(self, product, sources):
        self.reactions[product] = sources

    def showReactions(self):
        for key, values in self.reactions.items():
            print("{} made from {}".format(key,values))

    def produce(self, target, quantity, rest, depth=0, silent=True):
        if rest == None:
            rest = defaultdict(int)

        intendation = '____'*depth

        for key in self.reactions:
            if key[1] == target:
                if(not silent): print("{}want to produce {} {} and already have {} {}".format(intendation, quantity, target, rest[target], target))
                if(not silent): print("{}can do {} {} using: {} ".format(intendation, key[0], key[1], self.reactions[key]))
                
                if not (quantity - rest[target]) % key[0]:
                    rest[target] = 0
                    a = (quantity - rest[target]) // key[0]
                    if(not silent): print("{}glatt rest[{}]=0  a = {}".format(intendation, target, a))
                else:
                    a = ((quantity - rest[target]) // key[0]) + 1
                    rest[target] = key[0] - ((quantity - rest[target]) % key[0])
                    if(not silent): print("{}krumm rest[{}]={}  a = {}".format(intendation, target, rest[target], a))

                #print(a)
                if a == 0:
                    return 0, rest
                # multiple = quantity // key[0]
                # if quantity % key[0] != 0:
                #     multiple += 1
                # overproduced = multiple * key[0] - quantity
                
                if(not silent): print("{}Therefore produce '{} {}' {} times and keep {} pieces".format(intendation, key[0], key[1], a, rest[target]))
                #rest[key[1]] += overproduced
                cost = 0
                #depth = 0
                for source in self.reactions[key]:
                    if source[1] == "ORE":
                        if(not silent): print("{}Found {} ORE".format(intendation, source[0]*a))
                        return source[0]*a, rest
                    bla, rest = self.produce(source[1], source[0] * a, rest, depth=depth+1)
                    #print(bla)
                    cost += bla
                return cost, rest
        print(cost)

    def produceMax(self, availiable):
        # divide and conquer 
        low = availiable // self.produce("FUEL", 1, None)[0]
        high = 5 * low
        
        while high - low > 1:
            print("[{:10d}:{:10d}]".format(low, high))
            middle = (high + low) // 2
            cost = self.produce("FUEL", middle, None)[0]
            if cost <= availiable:
                low = middle
            else:
                high = middle
        cost = self.produce("FUEL", low, None)[0]
        print("{} produces {}".format(low, cost))
        return low
                

def load(string):
    #print(string)
    resourceTree = Resources()
    for line in string.split('\n'):
        #print(line)
        reaction = line.split(' => ')
        #print(reaction)
        needed = reaction[0].split(', ')
        sources = [(int(x.split()[0]), x.split()[1]) for x in needed]
        product = tuple((int(reaction[1].strip().split(' ')[0]), reaction[1].strip().split(' ')[1]))
        #print("generate {} from {}".format(product, sources))
        resourceTree.add(product, sources)
    resourceTree.showReactions()
    return resourceTree

def getOreForFuel(inp):
    myTree = load(inp)
    aa = myTree.produce("FUEL", 1, None)
    return aa[0]

def getMax(inp):
    myTree = load(inp)
    aa = myTree.produceMax(1000000000000)
    return aa

def run_small_test():
    print("small Test 1")
    print("############")
    inpA = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
    myTree = load(inpA)
    aa = myTree.produce("FUEL", 1, None)
    print(aa)
    # myTree.produce("A", 15)

def runPartOne():
    print("run Part One")
    print("############")
    with open('input', 'r') as f:
        inp = f.read()
    myTree = load(inp)
    aa = myTree.produce("FUEL", 1, None, silent=False)
    print(aa)

def run_small_test2():
    print("small Test 2")
    print("############")
    inpB = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
    myTree = load(inpB)
    aa = myTree.produceMax(1000000000000)
    print(aa)


def runPartTwo():
    print("run Part Two")
    print("############")
    with open('input', 'r') as f:
        inp = f.read()
    myTree = load(inp)
    aa = myTree.produceMax(1000000000000)
    print(aa)


if __name__ == '__main__':
    run_small_test()
    runPartOne()
    run_small_test2()
    runPartTwo()