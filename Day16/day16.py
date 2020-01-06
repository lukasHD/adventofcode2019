# --- Day 16: Flawed Frequency Transmission ---

import time
import cProfile

def int2list(inNumber):
    return list(map(int, list(inNumber)))

def phase(Inlist, debug=True):
    basePattern = [0, 1, 0, -1]
    outNumber = []
    for outDigit in range(len(Inlist)):
        applyPattern = []
        for i in basePattern:
            for _ in range(outDigit+1):
                applyPattern.append(i)
        #print("outDigit {}  ---  applypattern {}".format(outDigit, applyPattern))
        digit = 0
        length = len(applyPattern)
        for i, el in enumerate(Inlist):
            if debug: print("{}*{:2d} + ".format(el, applyPattern[(i+1)%len(applyPattern)]), end='')
            digit += (int(el)*applyPattern[(i+1)%length])
        realdigit = int(list(str(digit))[-1])
        if debug: print(" = {:3d}  ==> realdigit {}".format(digit, realdigit))
        outNumber.append(realdigit)
    if debug: print("outnumber = {}".format(outNumber))
    return outNumber


def loadInput(fname='input'):
    with open(fname, 'r') as f:
        l = f.read()
    print(l)
    return l

def huge(InList):
    return InList*10000

def hundertPhases(inlist):
    out = ''.join(map(str, phase(inlist, debug=False)))
    #print('.', end='')
    j = 0 
    print("{:4d}  {}".format(j, list(out)[0:8]))
    for j in range(1,100):
        out = ''.join(map(str, phase(out, debug=False)))
        print("{:4d}  {}".format(j, list(out)[0:8]))

    outList = list(out)[0:8]
    return outList


def run_small_test():
    print("small Test 1")
    print("############")
    aaa = int2list('12345678')
    print(aaa)
    phase(aaa)
    hundertPhases(aaa)

def runPartOne():
    print("run Part One")
    print("############")
    Inlist = loadInput()
    out2 = hundertPhases(Inlist)
    out = ''.join(map(str, out2))
    print(out)


def run_small_test2():
    print("small Test 2")
    print("############")
    for n in [1,10,100,1000,10000]:
        print("n = {:6d}  ---  ".format(n), end='')
        Input = '80871224585914546619083218645595'
        timeStart = time.time()
        out = ''.join(map(str, phase(int2list(Input*n), debug=False)))
        timeStop = time.time()
        print("1st phase took {:08.4f}     ".format(timeStop-timeStart), end='')
        timeStart = time.time()
        out = ''.join(map(str, phase(int2list(out), debug=False)))
        timeStop = time.time()
        print("2nd phase took {:08.4f}     ".format(timeStop-timeStart), end='')
        timeStart = time.time()
        out = ''.join(map(str, phase(int2list(out), debug=False)))
        timeStop = time.time()
        print("3rd phase took {:08.4f}".format(timeStop-timeStart))
        #cProfile.run("""phase(int2list('80871224585914546619083218645595'*10), debug=False)""")
    
    print(out)

def runPartTwo():
    print("run Part Two")
    print("############")


if __name__ == '__main__':
    #run_small_test()
    runPartOne()
    #run_small_test2()
    runPartTwo()