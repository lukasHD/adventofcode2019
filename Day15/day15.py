# --- Day 15: Oxygen System ---


from collections import defaultdict
from itertools import repeat
import random
import queue
import time 

def loadintCode(fname='input'):
    with open(fname, 'r') as f:
        l = list(f.read().split(','))
        p = [int(x) for x in l]
        return p

def constant_factory(value):
    return lambda: value

class Computer():
    def __init__(self, _prog):
        self.prog = defaultdict(int)
        for i in range(len(_prog)):
            self.prog[i] = int(_prog[i])
        self.inp           = queue.Queue()
        self.output        = queue.Queue()
        self.input_counter = 0
        self.halted        = False
        self.finished      = False
        self.idx           = 0
        self.base          = 0
        self.instrSet = {
            # code: (FUNCTION, #ofParams, Outputs, jumps)
            1:  (self.ADD, 3, True,  False),
            2:  (self.MUL, 3, True,  False),
            3:  (self.INP, 1, True,  False),
            4:  (self.OUT, 1, False, False),
            5:  (self.JPT, 2, False, True),
            6:  (self.JPF, 2, False, True),
            7:  (self.LES, 3, True,  False),
            8:  (self.EQL, 3, True,  False),
            9:  (self.ADJ, 1, False, False),
            99: (self.END, 0, False, True)
        }

    def ADD(self, vals):
        if len(vals) != 2: raise TypeError
        a,b = vals
        return a+b

    def MUL(self, vals):
        if len(vals) != 2: raise TypeError
        a,b = vals
        return a*b

    def INP(self, vals, interactive=True, value=0):
        if not interactive: 
            #print("simulate input value: {}".format(value))
            return value
        else: 
            print("Enter input: ")
            value = int(input())
            return value

    def OUT(self, vals, interactive=True):
        if len(vals) != 1: raise TypeError
        if not interactive:
            return  vals[0]
        else:
            print("Output is: {}".format(vals[0]))

    def JPT(self, vals):
        if vals[0] != 0: 
            return True
        else:
            return False

    def JPF(self, vals):
        if vals[0] == 0:
            return True
        else: 
            return False

    def LES(self, vals):
        if vals[0] < vals[1]:
            return 1
        else:
            return 0

    def EQL(self, vals):
        if vals[0] == vals[1]:
            return 1
        else:
            return 0

    def ADJ(self, vals):
        return vals[0]

    def END(self):
        #print("END")
        return "END"

    def decode(self,val):
        if val in self.instrSet.keys():
            # valid op code
            return self.instrSet[val]
        else:
            return None

    def run(self, debug=False, interactive=False):
        self.ignore = 0
        self.halted = False
        #output = []
        while not (self.finished or self.halted):
            val = self.prog[self.idx]
            if self.ignore > 0:
                self.ignore -= 1
                self.idx += 1
                continue
            #print("idx, val = {}, {}".format(self.idx, val))
            #if debug: printIndexValue(self.prog, self.idx)
            cmd = val%100
            op, numVar, writes, jumps = self.decode(cmd)
            if op == self.END:
                op()
                print("END END END")
                if debug: print(self.output.queue)
                self.finished = True
                if interactive == True:
                    return self.prog
                else:
                    if debug: print(self.output.queue)
                    return self.output
            modes = val//100
            mod= []
            while (modes > 0):
                tmp = modes%10
                if tmp not in [0, 1, 2]: raise TypeError
                mod.append(tmp)
                modes = modes//10
            vars = []
            for i in range(numVar):
                try:
                    m = mod[i]
                except IndexError:
                    m = 0
                if m == 0:
                    vars.append(self.prog[self.prog[self.idx+1+i]])
                elif m == 1:
                    vars.append(self.prog[self.idx+1+i])
                elif m == 2:
                    vars.append(self.prog[self.base + self.prog[self.idx+1+i]])
                else: 
                    raise RuntimeError
            if op == self.ADJ:
                # adjust the base by the value of the parameter 
                self.base = self.base + vars[0]
            elif writes:
                # an opcode that writes to last parameter
                if op == self.INP and interactive == False:
                    if self.inp.empty():
                        #print("empty")
                        return self.output
                    _value = self.inp.get(block=False)
                    #print("InputValue = {}".format(_value))
                    #if debug: print("{} {}".format(numVar, vars))
                    if m == 0:
                        self.prog[self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=_value)
                    elif m == 2:
                        self.prog[self.base + self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=_value)
                    else:
                        raise RuntimeError
                else:
                    if m == 0:
                        self.prog[self.prog[self.idx+numVar]] = op(vars[:-1])
                    elif m == 2:
                        self.prog[self.base + self.prog[self.idx+numVar]] = op(vars[:-1])
                    else:
                        raise RuntimeError

            elif jumps:
                #print("JUMP")
                if op(vars[:-1]):
                    self.idx = vars[-1]
                    continue
            else:
                if op == self.OUT and interactive == False:
                    value = op(vars, interactive=False)
                    #print(value)
                    self.output.put(value)

                    if debug: print(self.output.queue)
                    if self.output.qsize() == 3:
                        self.halted = True
                        #self.finished = True
                        #self.ignore = numVar
                        self.idx += 2
                        return self.output
                    self.idx += 0
                    #return output[-1] 
                else:
                    op(vars)
            self.ignore = numVar
            self.idx += 1

class Robot():

    def __init__(self,_intCode=[]):
        self.screen   = defaultdict(int)
        self.intCode  = _intCode.copy()
        self.computer = Computer(self.intCode)
        #self.map = defaultdict(lambda: defaultdict(int))
        self.map = defaultdict(lambda: defaultdict(constant_factory(int(-1))))
        
        self.map[0][0] = 1
        self.position = [0,0] # x to the right and y down ==> N is up(-y) S is down(+y) E is right(+x) W is left(-x)
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0

    def getCharFromValue(self, value):
        if value == -1:
            return '   '
        elif value == 0:
            return '███'
        elif value == 1:
            return ' ◦ '
        elif value == 2:
            return ' ◎ '
        else:
            raise ValueError

    def turnRight(self, direction):
        if   direction == 1:
            return 4
        elif direction == 2:
            return 3
        elif direction == 3:
            return 1
        elif direction == 4:
            return 2

    def step(self, direction, debug=True):
        # north (1), south (2), west (3), and east (4)
        if direction not in [1,2,3,4]:
            raise ValueError
        if   direction == 1:
            if debug: print("try North ... ",end='')
        elif direction == 2:
            if debug: print("try South ... ",end='')
        elif direction == 3:
            if debug: print("try West  ... ",end='')
        elif direction == 4:
            if debug: print("try East  ... ",end='')
        self.computer.inp.put(direction)
        self.computer.run()
        status = self.computer.output.get()
        newPos = list(self.position)
        if   direction == 1:
            newPos[1] -= 1
            self.ymin = min(self.ymin, newPos[1])
        elif direction == 2:
            newPos[1] += 1
            self.ymax = max(self.ymax, newPos[1])
        elif direction == 3:
            newPos[0] -= 1
            self.xmin = min(self.xmin, newPos[0])
        elif direction == 4:
            newPos[0] += 1
            self.xmax = max(self.xmax, newPos[0])
        if debug: print("self.map[{}][{}] = {}    ".format(newPos[1], newPos[0], status), end='')
        self.map[newPos[1]][newPos[0]] = status
        if status == 0:
            if debug: print("Wall")
            return 0
        elif status == 1:
            # advanced in this direction
            self.position = list(newPos)
            if debug: print("new Position is {}".format(self.position))
            return 1
        elif status == 2:
            # found the oxygen
            if debug: print("Oxygen")
            return 2

    def TaT(self, start=[0,0], goal=2):
        # Tarry & Trémaux Algorithmus
        # Der Algorithmus startet willkürlich an einem Knoten und folgt einem möglichen Pfad (Gang) und markiert dabei jede Kante in welcher Richtung sie bereits betreten worden ist.
        # Kommt man an einen Knoten (Kreuzung), wählt man einen beliebigen Pfad aus, der noch nicht betreten worden ist. Sind alle Kanten schon betreten, dann eine auswählen, die bis jetzt nur einmal in die Gegenrichtung betreten worden ist.
        # Trifft man auf eine Sackgasse oder auf einen schon besuchten Gang, dann muss man zurück zur letzten Kreuzung.
        # Man darf keinen Pfad betreten, der schon in beide Richtungen besucht wurde.
        # Der Algorithmus ist beendet, wenn man wieder am Startpunkt angekommen ist.
        return 1


    def explore(self):
        print("Start Exploring")
        currentDirection = 1
        count = 0
        while (True):
            if count > 30:
                break
            count += 1
            nextDirection = self.turnRight(currentDirection)
            if self.step(nextDirection) == 0:
                if self.step(currentDirection) == 0:
                    currentDirection = nextDirection    
                    #continue
            else:
                currentDirection = nextDirection

    def getPossible(self):
        possible = []
        for i in [1,2,3,4]:
            if self.step(i, False) == 1:
                possible.append(i)
                # return to origin
                if i == 1:
                    self.step(2, False)
                elif i == 2:
                    self.step(1, False)
                elif i == 3:
                    self.step(4, False)
                elif i == 4:
                    self.step(3, False)
        return possible


    def exploreRand(self, maxcount=3000):
        print("Start Exploring")
        count = 0
        lastDirection = 1
        while (True):
            if count > maxcount:
                break
            count += 1
            directions = self.getPossible()
            #print(directions)
            if len(directions) == 1:
                self.step(directions[0], debug=False)
                lastDirection = directions[0]
                continue
            emergency = 0
            if lastDirection == 1:
                directions.remove(2)
                emergency = 2
            elif lastDirection == 2:
                directions.remove(1)
                emergency = 1
            elif lastDirection == 3:
                directions.remove(4)
                emergency = 4
            elif lastDirection == 4:
                directions.remove(3)
                emergency = 3
            for _ in range(len(directions)):
                #print("choose from {}".format(directions))
                nextdir = random.choice(directions)
                directions.remove(nextdir)
                emerg = True
                if self.step(nextdir, debug=False) == 1:
                    lastDirection = nextdir
                    #print("break")
                    emerg=False
                    break
            if emerg:
                self.step(emergency, debug=False)
                lastDirection = emergency

    def printMinMax(self):
        print("x = [{}, {}]    y = [{}, {}]".format(self.xmin, self.xmax, self.ymin, self.ymax))

    def printMap(self, buffer = 1):
        self.printMinMax()
        for y in range(self.ymin -buffer, self.ymax +buffer ):
            for x in range(self.xmin -buffer, self.xmax +buffer):
                print("{}".format(self.getCharFromValue(self.map[y][x])),end='')
            print()


def run_small_test():
    print("small Test 1")
    print("############")
    print("run Part One")
    print("############")
    intcode = loadintCode()
    robot = Robot(intcode)
    print(robot.step(1))
    print(robot.step(4))
    print(robot.step(2))
    print(robot.step(3))
    print(robot.step(1))
    print(robot.step(2))
    print(robot.printMap())


def runPartOne():
    print("run Part One")
    print("############")
    intcode = loadintCode()
    robot = Robot(intcode)
    robot.exploreRand()
    print(robot.printMap())

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