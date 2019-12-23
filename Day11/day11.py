# --- Day 11: Space Police ---

# You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of square panels on the side of your ship, detect the color of its current panel, and paint its current panel black or white. (All of the panels are currently black.)

# The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will output two values:

#     First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
#     Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.

# black = 0
# white = 1
# all is black in the beginning

# 0 => turn left 
# 1 => turn right

from collections import defaultdict
import queue

def loadintCode(fname='input'):
    with open(fname, 'r') as f:
        l = list(f.read().split(','))
        p = [int(x) for x in l]
        return p

class Computer():
    def __init__(self, _prog):
        self.prog = defaultdict(int)
        for i in range(len(_prog)):
            self.prog[i] = int(_prog[i])
        self.inp           = queue.Queue()
        self.output        = 0
        self.input_counter = 0
        self.halted        = False
        self.finisehd      = False
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
        ignore = 0
        output = []
        while not self.finisehd:
            val = self.prog[self.idx]
            if ignore > 0:
                ignore -= 1
                self.idx += 1
                continue
            #if debug: printIndexValue(self.prog, self.idx)
            cmd = val%100
            op, numVar, writes, jumps = self.decode(cmd)
            if op == self.END:
                op()
                #print("END END END")
                if debug: print(output)
                self.finisehd = True
                if interactive == True:
                    return self.prog
                else:
                    if debug: print(output)
                    return output
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
                        return output
                    #if debug: print("{} {}".format(numVar, vars))
                    if m == 0:
                        self.prog[self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=self.inp.get(block=False))
                    elif m == 2:
                        self.prog[self.base + self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=self.inp.get(block=False))
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
                    output.append(op(vars, interactive=False))
                    if debug: print(output)
                    #self.halted = True
                    self.idx += 0
                    #return output[-1] 
                else:
                    op(vars)
            ignore = numVar
            self.idx += 1


class Painter:

    def __init__(self,_intCode=[]):
        self.direction = '^'
        self.position = [0,0]
        self.painted = defaultdict(int)
        self.intCode = _intCode.copy()
        self.computer = Computer(self.intCode)

    def paint_black(self):
        self.painted[tuple(self.position)] = 0

    def paint_white(self):
        self.painted[tuple(self.position)] = 1
    
    def paint(self, color):
        self.painted[tuple(self.position)] = color

    def turn_left(self):
        if self.direction == '^':
            self.direction = '<'
        elif self.direction == '<':
            self.direction = 'v'
        elif self.direction == 'v':
            self.direction = '>'
        elif self.direction == '>':
            self.direction = '^'

    def turn_right(self):
        if self.direction == '^':
            self.direction = '>'
        elif self.direction == '>':
            self.direction = 'v'
        elif self.direction == 'v':
            self.direction = '<'
        elif self.direction == '<':
            self.direction = '^'
    
    def advance(self):
        oldPos = self.position
        if self.direction == '^':
            self.position[0] = oldPos[0]
            self.position[1] = oldPos[1] - 1            
        elif self.direction == '>':
            self.position[0] = oldPos[0] + 1
            self.position[1] = oldPos[1]
        elif self.direction == 'v':
            self.position[0] = oldPos[0]
            self.position[1] = oldPos[1] + 1
        elif self.direction == '<':
            self.position[0] = oldPos[0] - 1
            self.position[1] = oldPos[1]

    def color_from_value(self, value):
        if value == 0 or value == None:
            return '..'
        elif value == 1:
            return '##'
        else:
            raise ValueError("Color does not exist")

    def draw(self, xmin = -25, xmax = 25, ymin = -25, ymax = 25):
        # check constraints
        if xmax-xmin <=0 or ymax-ymin <= 0:
            raise ValueError("Each dimension has to be bigger than 0, min has to be lower than max")
        print()
        print()
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                print("{}".format(self.color_from_value(self.painted[(x,y)])), end='')
            print()
        print()
            
    def draw_with_border(self, border = 2):
        xmin = min(self.painted.keys(), key= lambda x: x[0])[0] - border
        xmax = max(self.painted.keys(), key= lambda x: x[0])[0] + border

        ymin = min(self.painted.keys(), key= lambda x: x[1])[1] - border
        ymax = max(self.painted.keys(), key= lambda x: x[1])[1] + border
        print()
        print()
        print("x: [{}, {}]    y: [{}, {}]".format(xmin, xmax, ymin, ymax))
        self.draw(xmin, xmax, ymin, ymax)

    def step(self, debug=False):
        currentColor = self.painted[tuple(self.position)]
        if currentColor == None:
            currentColor = 0
        self.computer.inp.put(currentColor)
        out = self.computer.run(debug=False, interactive=False)
        self.paint(out[0])
        if debug: print("paint pos {} with color {}".format(self.position, out[0]))
        if debug: print("{}: {}".format(len(self.painted), self.painted.keys))
        if out[1] == 0:
            self.turn_left()
        elif out[1] == 1:
            self.turn_right()
        else:
            raise ValueError("strange strange strange ...")
        self.advance()

    def run(self):
        while not self.computer.finisehd:
            print('*', end='')
            self.step()


def run_small_test():
    print("small Test 1")
    print("############")

    painter = Painter()
    painter.painted[(0,1)] = 1
    painter.painted[(0,-1)] = 1
    painter.painted[(1,0)] = 1
    painter.painted[(-1,0)] = 1
    print(painter.painted)

    painter.draw()


def runPartOne():
    print("run Part One")
    print("############")
    print("load Code")
    intCode = loadintCode('input11')
    print("create painter")
    painter = Painter(intCode)
    for _ in range(10):
        painter.step(debug=True)
    painter.run()
    print("count of painted values")
    print(len(painter.painted))
    painter.draw_with_border()
    print("count of painted values")
    print(len(painter.painted))


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