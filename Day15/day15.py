# --- Day 15: Oxygen System ---


from collections import defaultdict
from itertools import repeat
from tkinter import Tk, Button, Message, Y, RIGHT, Frame, BOTH, LEFT
import random
import queue
import time 
import threading

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
        self.tree = None
        self.position = [0,0] # x to the right and y down ==> N is up(-y) S is down(+y) E is right(+x) W is left(-x)
        self.oxygen = None
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.count = 0
        self.lastDirection = 1

        self.queueGUI = queue.Queue()
        self.decisionPoints = []
        self.listOfDirections =[]

    def getCharFromValue(self, value):
        if value == -1:
            return '   '
        elif value == 0:
            return '███'
        elif value == 1:
            return ' ◦ '
        elif value == 2:
            #return ' ◎ '
            return ' W '
        elif value == 5:
            return ' ~ '
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

    def turnLeft(self, direction):
        if   direction == 1:
            return 3
        elif direction == 2:
            return 4
        elif direction == 3:
            return 2
        elif direction == 4:
            return 1

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
            self.lastDirection = direction
            if debug: print("new Position is {}".format(self.position))
            return 1
        elif status == 2:
            # found the oxygen
            self.position = list(newPos)
            self.oxygen = list(newPos)
            self.lastDirection = direction
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
        backup = self.lastDirection
        possible = []
        for i in [1,2,3,4]:
            if self.step(i, False) != 0:
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
        self.lastDirection = backup
        return possible

    def exploreRand(self, maxcount=3000):
        #print("Start Exploring\n\n\n")
        self.count = 0
        while (True):
            if self.count > maxcount:
                break
            self.count += 1
            directions = self.getPossible()
            #print("availiable {}  last direction {}".format(directions, self.lastDirection))
            if len(directions) == 1:
                self.step(directions[0], debug=False)
                self.lastDirection = directions[0]
                continue
            emergency = 0
            if self.lastDirection == 1:
                directions.remove(2)
                emergency = 2
            elif self.lastDirection == 2:
                directions.remove(1)
                emergency = 1
            elif self.lastDirection == 3:
                directions.remove(4)
                emergency = 4
            elif self.lastDirection == 4:
                directions.remove(3)
                emergency = 3
            for _ in range(len(directions)):
                #print("choose from {}".format(directions))
                nextdir = random.choice(directions)
                directions.remove(nextdir)
                emerg = True
                if self.step(nextdir, debug=False) != 0:
                    self.lastDirection = nextdir
                    #print("break")
                    emerg=False
                    break
            if emerg:
                self.step(emergency, debug=False)
                self.lastDirection = emergency

    def getReverse(self, direction):
        if direction == 1:
            return 2
        elif direction == 2:
            return 1
        elif direction == 3:
            return 4
        elif direction == 4:
            return 3

    def find(self):
        print("try to find all")
        directionStack = []

        x = threading.Thread(target=self.guiThread)
        #threads.append(x)
        x.start()

        for i in range(3,0):
            print("put {}".format(i))
            self.queueGUI.put(str(i))
            time.sleep(1)

        counter = 0
        start_time = time.time()
        backtrack = False
        searchPos = []
        openDirections = [] 
        steptime = 0.05
        while counter < 1500:
            while (now := time.time()) - start_time <= steptime:
                time.sleep(0.01)
            start_time = now
            counter += 1
            if backtrack:
                print("I'm here {}".format(self.position))
                if self.position == searchPos:
                    print("Backtrack finisehd - move in the open direction")
                    # return here for recursive functions
                    backtrack = False
                    move = openDirections.pop()
                    self.step(move)
                    directionStack.append(move)
                    if len(openDirections) > 0:
                        self.decisionPoints.append([self.position, openDirections])
                else:
                    move = directionStack.pop()
                    self.step(self.getReverse(move), debug=True)
                self.queueGUI.put(self.getImage())
                continue
            # if len(possible) == 1:
            #     self.step(possible[0], debug=True)
            # else: 
            possible = self.getPossible()
            try:
                emergerncy = self.getReverse(self.lastDirection)
                possible.remove(emergerncy)
            except:
                pass
            if len(possible) == 1:
                directionStack.append(possible[0])
                self.step(possible[0], debug=False)
            elif len(possible) > 1:
                #steptime = 0.5
                # make a descision
                self.decisionPoints.append([self.position, possible[1:]])
                move = possible[0] # this is the decision
                directionStack.append(move)
                self.step(move, debug=False)
            else:
                searchPos, openDirections = self.decisionPoints.pop()
                print("I'm stuck at {} - backtrack to position {}".format(self.position, searchPos))
                backtrack = True
                # while self.position != searchPos:
                #     self.step(self.getReverse(directionStack.pop()))
                # print("finished Backtrack - availiable directions {}".format(openDirections))
                # time.sleep(2)
                # self.step(openDirections[0])


            self.queueGUI.put(self.getImage())

        print("finisehd")

        x.join()

    def find2(self, visual=True):
        print("try to find all")
        if visual:
            x = threading.Thread(target=self.guiThread)
            #threads.append(x)
            x.start()
            for i in range(3,0):
                print("put {}".format(i))
                self.queueGUI.put(str(i))
                time.sleep(1)

        counter = 0
        start_time = time.time()
        currentDirection = 1
        steptime = 0.0001
        if visual: steptime = 0.02
        while counter < 3000:
            if self.position == [0,0] and counter > 1500:
                break
            while (now := time.time()) - start_time <= steptime and visual:
                time.sleep(0.01)
            start_time = now
            counter += 1
            
            if visual: self.queueGUI.put(self.getImage())
            self.getPossible()
            try:
                nextDirection = self.turnRight(currentDirection)
                if self.step(nextDirection, debug=False) != 0:
                    currentDirection = nextDirection
                    continue
                if self.step(currentDirection, debug=False) != 0:
                    continue
                nextDirection = self.turnLeft(currentDirection)
                if self.step(nextDirection, debug=False) != 0:
                    currentDirection = nextDirection
                    continue
                nextDirection = self.getReverse(currentDirection)
                if self.step(nextDirection, debug=False) != 0:
                    currentDirection = nextDirection
                    continue
            except:
                pass
        if visual: self.queueGUI.put(self.getImage())
        print("finisehd")
        print("Took me {} steps to discover the labyrith".format(counter))

        if visual: x.join()

    def convert2tree(self):
        print("Try to convert map to a tree we can search")
        #if self.oxygen == None:
        #    raise ValueError("Should explore first")
        tree = defaultdict(list)
        buffer = 1
        self.printMinMax()
        for y in range(self.ymin -buffer, self.ymax +buffer ):
            for x in range(self.xmin -buffer, self.xmax +buffer):
                if self.map[y][x] <= 0:
                    # this is not a valid node
                    continue
                else: 
                    if self.map[y-1][x] > 0:
                        tree[(x,y)].append((x,y-1))
                    if self.map[y+1][x] > 0:
                        tree[(x,y)].append((x,y+1))
                    if self.map[y][x-1] > 0:
                        tree[(x,y)].append((x-1,y))
                    if self.map[y][x+1] > 0:
                        tree[(x,y)].append((x+1,y))
        #print(tree)
        self.tree = tree

    def BFS(self):
        if self.tree == None:
            raise ValueError("convert to tree first")

        # finds shortest path between 2 nodes of a graph using BFS
        def bfs_shortest_path(graph, start, goal):
            print("{} --- {} --- {}".format(graph, start, goal))
            # keep track of explored nodes
            explored = []
            # keep track of all the paths to be checked
            queue = [[start]]
        
            # return path if start is goal
            if start == goal:
                return "That was easy! Start = goal"
        
            # keeps looping until all possible paths have been checked
            while queue:
                # pop the first path from the queue
                path = queue.pop(0)
                # get the last node from the path
                node = path[-1]
                if node not in explored:
                    neighbours = graph[node]
                    # go through all neighbour nodes, construct a new path and
                    # push it into the queue
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        queue.append(new_path)
                        # return path if neighbour is goal
                        if neighbour == goal:
                            return new_path
        
                    # mark node as explored
                    explored.append(node)
        
            # in case there's no path between the 2 nodes
            return "So sorry, but a connecting path doesn't exist :("

        aaaaaa = bfs_shortest_path(self.tree, (0,0), tuple(self.oxygen))
        print(aaaaaa)
        print(len(aaaaaa)-1)

    def fillOxygen(self, visual=True):
        if visual:
            x = threading.Thread(target=self.guiThread)
            #threads.append(x)
            x.start()
            for i in range(3,0):
                print("put {}".format(i))
                self.queueGUI.put(str(i))
                time.sleep(1)
        
        start_time = time.time()
        steptime = 0.0001
        if visual: steptime = 0.02
            
        if visual: self.queueGUI.put(self.getImage())

        x,y = list(self.oxygen)
        self.map[y][x] = 5
        counter = 0
        wavefront = [tuple(self.oxygen)]
        for _ in range(20):
            while (now := time.time()) - start_time <= steptime and visual:
                time.sleep(0.01)
            start_time = now
            # fill next neighbours
            nextWavefront = []
            print(wavefront)
            while len(wavefront) > 0:
                current = wavefront.pop()
                for neighbor in self.tree[current]:
                    print(neighbor)
                    # fill neighbor mit 5 and add to next wavefront
                    self.map[neighbor[1]][neighbor[0]] = 5
                    nextWavefront.append(neighbor)
                    print("fill")
            wavefront = nextWavefront.copy()
            if visual: self.queueGUI.put(self.getImage())
            counter += 1
        
        if visual: self.queueGUI.put(self.getImage())
        print("finisehd")
        print("Took me {} steps to discover the labyrith".format(counter))

        if visual: x.join()


    def guiThread(self):
        root = Tk()
        pane = Frame(root) 
        pane.pack(fill = BOTH, expand = True) 
        exit_button = Button(pane, text='Exit Program', command=root.destroy)
        exit_button.pack(side = LEFT, expand = True, fill = BOTH)
        msg = Message(root, text="TEST TEST TEST")
        msg.config(font=('Consolas', 10, ''))
        msg.pack()

        def updateImage():
            #print("in updateImage()")
            if not self.queueGUI.empty():
                while not self.queueGUI.empty():
                    imgText = self.queueGUI.get()
                #print("set Text to {}".format(imgText))
                msg.configure(text=imgText)
                #if len(self.queueGUI.queue):
                    #print("clear queue")
                    #self.queueGUI.queue.clear()
            #else:
                #print("queue empty")
            root.after(100, updateImage)

        root.after(100, updateImage)
        root.mainloop()


    def printMinMax(self):
        print("x = [{}, {}]    y = [{}, {}]".format(self.xmin, self.xmax, self.ymin, self.ymax))

    def printMap(self, buffer = 1):
        self.printMinMax()
        for y in range(self.ymin -buffer, self.ymax +buffer ):
            for x in range(self.xmin -buffer, self.xmax +buffer):
                print("{}".format(self.getCharFromValue(self.map[y][x])),end='')
            print()

    def getImage(self, buffer = 1):
        a= "          x = [{}, {}]    y = [{}, {}]\n\n".format(self.xmin, self.xmax, self.ymin, self.ymax)
        for y in range(self.ymin -buffer, self.ymax +buffer ):
            for x in range(self.xmin -buffer, self.xmax +buffer):
                if x == self.position[0] and y == self.position[1]:
                    a += " D "
                    continue
                a += "{}".format(self.getCharFromValue(self.map[y][x]))
            a += "\n"
        return a

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
    robot.convert2tree()


def runPartOne():
    print("run Part One")
    print("############")
    intcode = loadintCode()
    robot = Robot(intcode)
    robot.find2(visual=False)
    robot.convert2tree()
    print(
        robot.tree[(-20,14)]
    )
    robot.BFS()
    # fill the ship with oxygen (Part2)
    robot.fillOxygen()

def run_small_test2():
    print("small Test 2")
    print("############")
    intcode = loadintCode()
    robot = Robot(intcode)
    root = Tk()
    pane = Frame(root) 
    pane.pack(fill = BOTH, expand = True) 
    
    def N(_event=None):
        robot.step(1)
        robot.getPossible()
        img = robot.getImage()
        msg.configure(text=img)
    def S(_event=None):
        robot.step(2)
        robot.getPossible()
        img = robot.getImage()
        msg.configure(text=img)
    def W(_event=None):
        robot.step(3)
        robot.getPossible()
        img = robot.getImage()
        msg.configure(text=img)
    def E(_event=None):
        robot.step(4)
        robot.getPossible()
        img = robot.getImage()
        msg.configure(text=img)
    def rand(_event=None):
        robot.exploreRand(5)
        img = robot.getImage()
        msg.configure(text=img)
    def find(_event=None):
        robot.find()
        img = robot.getImage()
        msg.configure(text=img)

    N_button = Button(pane, text='North', command=N)
    N_button.pack(side = LEFT, expand = True, fill = BOTH)
    S_button = Button(pane, text='South', command=S)
    S_button.pack(side = LEFT, expand = True, fill = BOTH)

    E_button = Button(pane, text='East', command=E)
    E_button.pack(side = LEFT, expand = True, fill = BOTH)
    W_button = Button(pane, text='West', command=W)
    W_button.pack(side = LEFT, expand = True, fill = BOTH)

    R_button = Button(pane, text='RAND', command=rand)
    R_button.pack(side = LEFT, expand = True, fill = BOTH)
    F_button = Button(pane, text='Find', command=find)
    F_button.pack(side = LEFT, expand = True, fill = BOTH)

    root.bind('w', N)
    root.bind('s', S)
    root.bind('a', W)
    root.bind('d', E)
    root.bind('r', rand)

    exit_button = Button(pane, text='Exit Program', command=root.destroy)
    exit_button.pack(side = LEFT, expand = True, fill = BOTH)

    robot.step(3)
    robot.step(3)
    robot.step(3)
    image = robot.getImage()

    msg = Message(root, text=image)
    msg.config(font=('Consolas', 10, ''))
    msg.pack()
    root.mainloop()

def runPartTwo():
    print("run Part Two")
    print("############")


if __name__ == '__main__':
    run_small_test()
    runPartOne()
    #run_small_test2()
    runPartTwo()