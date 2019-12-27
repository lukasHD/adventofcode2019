# --- Day 13: Care Package ---


from collections import defaultdict
import queue
import time 

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
                        print("empty")
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


class Arcade:

    def __init__(self,_intCode=[]):
        self.screen   = defaultdict(int)
        self.intCode  = _intCode.copy()
        self.computer = Computer(self.intCode)
        self.ballX    = 0
        self.paddleX  = 0
    
    def paint(self, x, y, tile_id):
        self.screen[tuple([x, y])] = tile_id

    def get_joystick(self):
        if self.ballX < self.paddleX:
            # move to left
            return -1
        elif self.ballX > self.paddleX:
            # move to right
            return 1
        elif self.ballX == self.paddleX:
            # keep paddle
            return 0
        else:
            raise ValueError

    def color_from_value(self, value):
        if value == 0 or value == None:
            # 0 is an empty tile. No game object appears in this tile.
            return ' '
        elif value == 1:
            # 1 is a wall tile. Walls are indestructible barriers.
            return '▮' 
        elif value == 2:
            # 2 is a block tile. Blocks can be broken by the ball.
            return '~'
        elif value == 3:
            # 3 is a horizontal paddle tile. The paddle is indestructible.
            return '_'
        elif value == 4:
            # 4 is a ball tile. The ball moves diagonally and bounces off objects.
            return '*'
        else:
            raise ValueError("Color does not exist")

    def draw(self, xmin = -25, xmax = 25, ymin = -25, ymax = 25):
        # check constraints
        if xmax-xmin <=0 or ymax-ymin <= 0:
            raise ValueError("Each dimension has to be bigger than 0, min has to be lower than max")
        print()
        print()
        for y in range(ymin, ymax):
            cnt = 0
            for x in range(xmin, xmax):
                cnt += 1
                if x == -1 and y == 0:
                    print("  Score: {}". format(self.screen[(x,y)]))
                    #print("***************************************")
                    for _ in range(cnt):
                        print("{}".format(self.color_from_value(0)), end='')
                else:
                    print("{}".format(self.color_from_value(self.screen[(x,y)])), end='')
            print()
        print()
            
    def draw_with_border(self, border = 2):
        xmin = min(self.screen.keys(), key= lambda x: x[0])[0] - border
        xmax = max(self.screen.keys(), key= lambda x: x[0])[0] + border + 1

        ymin = min(self.screen.keys(), key= lambda x: x[1])[1] - border
        ymax = max(self.screen.keys(), key= lambda x: x[1])[1] + border + 1
        print()
        print()
        print("x: [{}, {}]    y: [{}, {}]".format(xmin, xmax, ymin, ymax))
        self.draw(xmin, xmax, ymin, ymax)

    def step(self, debug=False):
        out = self.computer.run(debug=False, interactive=False)
        if out.qsize() < 3:
            print("AAAAAAAAAA")
            return
        x      = out.get()
        y      = out.get()
        tileID = out.get()
        if x == -1 and y == 0:
            # print the counter
            print ("Current score: {}".format(tileID))
        if tileID == 4: 
            # is the ball -- update its position
            self.ballX = x
        if tileID == 3:
            # is the paddle
            self.paddleX = x
        #print("[{}, {}] = {}".format(x, y, tileID))
        self.paint(x, y, tileID)

    def stepSimulated(self, debug=False):
        updateInput = False
        out = self.computer.run(debug=False, interactive=False)
        if out.qsize() < 3:
            print("AAAAAAAAAA")
            return
        x      = out.get()
        y      = out.get()
        tileID = out.get()
        #if x == -1 and y == 0:
            # print the counter
            #print ("Current score: {}".format(tileID))
        if tileID == 4: 
            # is the ball -- update its position
            self.ballX = x
            updateInput = True
        if tileID == 3:
            # is the paddle
            self.paddleX = x
            updateInput = True
        #print("[{}, {}] = {}".format(x, y, tileID))
        self.paint(x, y, tileID)
        if updateInput:
            if self.computer.inp.qsize() > 0:
                # delete the queue and enqueue the new input
                self.computer.inp.queue.clear()
            self.computer.inp.put(self.get_joystick())


    def run(self):
        while not self.computer.finished:
            print('*', end='')
            self.step()
            #print(self.computer.finished)

    def play(self):
        startTime = int(time.time()*1000)
        print(startTime)
        time.sleep(1)
        now = int(time.time()*1000)
        print(now - startTime)
        startTime = int(time.time()*1000)
        while not self.computer.finished:
            #print('*', end='')
            now = int(time.time()*1000)
            if now - startTime > 500:
                for _ in range(5):
                    print()
                self.draw_with_border(0)
                startTime = int(time.time()*1000)
            self.stepSimulated()
            #print(self.computer.finished)



def run_small_test():
    print("small Test 1")
    print("############")

def runPartOne():
    print("run Part One")
    print("############")
    print("load Code")
    intCode = loadintCode('input')
    print("create arcade")
    arcade = Arcade(intCode)
    #for _ in range(10):
    arcade.step(debug=True)
    arcade.run()
    arcade.draw_with_border()

    res = 0
    for elem in arcade.screen.values():
        if elem == 2: 
            res += 1
    print(res)

def run_small_test2():
    print("small Test 2")
    print("############")

def runPartTwo():
    print("run Part Two")
    print("############")
    print("load Code")
    intCode = loadintCode('input')
    print("create arcade")
    
    arcade = Arcade(intCode)
    arcade.computer.prog[0] = 2
    arcade.play()
    arcade.draw_with_border(border=2)


if __name__ == '__main__':
    run_small_test()
    runPartOne()
    run_small_test2()
    runPartTwo()