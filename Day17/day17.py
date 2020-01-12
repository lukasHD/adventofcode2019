# --- Day 17: Set and Forget ---

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
                    # if self.output.qsize() == 3:
                    #     self.halted = True
                    #     #self.finished = True
                    #     #self.ignore = numVar
                    #     self.idx += 2
                    #     return self.output
                    self.idx += 0
                    #return output[-1] 
                else:
                    op(vars)
            self.ignore = numVar
            self.idx += 1

class Robot():

    def __init__(self, intcode):
        self.computer = Computer(intcode)
        self.queueGUI = queue.Queue()

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
            return 'OOO'
        else:
            raise ValueError

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

        def updateImage2():
            #print("in updateImage()")
            if not self.computer.output.empty():
                oldLine = ''
                imgText = ''
                while True:
                    try:
                        el = self.computer.output.get()
                        current =  chr(el)
                    except:
                        print("bla bla bla {}".format(el))
                        continue
                    if current in ['<', '>', 'v', '^']:
                        bla = '█'+current+'█'
                    elif current in ['x', 'X']:
                        bla = ' '+current+' '
                    elif current == '#':
                        bla = '███'
                    elif current == '\n':
                        bla = current
                    else:
                        bla = '   '
                    imgText += bla
                    if current == "\n" and oldLine == "\n":
                        break
                    oldLine = current
                #print("set Text to {}".format(imgText))
                msg.configure(text=imgText)
                #if len(self.queueGUI.queue):
                    #print("clear queue")
                    #self.queueGUI.queue.clear()
            #else:
                #print("queue empty")
            root.after(100, updateImage2)

        root.after(100, updateImage2)
        root.mainloop()

    def getImage(self):
        return ''.join(list(map(chr, list(self.computer.output.queue) )))

    def run(self, visual=True):
        if visual:
            print("Start GUI Thread")
            x = threading.Thread(target=self.guiThread)
            x.start()
            for i in range(3,0):
                print("put {}".format(i))
                self.queueGUI.put(str(i))
                time.sleep(1)

        mainProg = "A,A,B,C,B,C,B,C,B,A\n"
        progA    = "L,10,L,8,R,8,L,8,R,6\n"
        progB    = "R,6,R,8,R,8\n"
        progC    = "R,6,R,6,L,8,L,10\n"
        contOut  = "y\n"

        command = mainProg + progA + progB + progC + contOut

        for char in command:
            val = ord(char)
            print(val,end='')
            self.computer.inp.put(val)
        
        print("\n\nRun Computer\n")
        self.computer.run()

        if visual: self.queueGUI.put(self.getImage())

        if visual: x.join()

def getString(liste):
    return ''.join(list(map(chr, liste)))

def str2array(string):
    out = string.split('\n')
    out = list(map(list, out))
    return out

def printNice(liste):
    for el in liste:
        print("{}".format(chr(el)), end='' )

def run_small_test():
    print("small Test 1")
    print("############")


def runPartOne():
    print("run Part One")
    print("############")
    code = loadintCode()
    computer = Computer(code)
    computer.run()
    printNice(list(computer.output.queue))
    a = str2array(getString(list(computer.output.queue))[:-2])
    result = 0
    for y, line in enumerate(a):
        for x, el in enumerate(line):
            if el == '#':
                counter = 0
                try: 
                    if a[y-1][x] == '#': counter += 1
                except:
                    pass
                try: 
                    if a[y+1][x] == '#': counter += 1
                except:
                    pass
                try: 
                    if a[y][x-1] == '#': counter += 1
                except:
                    pass
                try: 
                    if a[y][x+1] == '#': counter += 1
                except:
                    pass
                if counter == 4:
                    print("Intersection at x = {} y = {}".format(x, y))
                    result += x*y
    print(result)
        #     if el == '#': 
        #         print("███", end='')
        #     elif el == '.':
        #         print(' ◦ ', end='')
        # print()
    #print(repr(a))

def run_small_test2():
    print("small Test 2")
    print("############")

def runPartTwo():
    print("run Part Two")
    print("############")
    code = loadintCode()
    # switch to interactive mode
    code[0] = 2
    #print(repr(code))
    robot = Robot(code)
    robot.run()


if __name__ == '__main__':
    #run_small_test()
    runPartOne()
    #run_small_test2()
    runPartTwo()