# --- Day 16: Flawed Frequency Transmission ---

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
        for i, el in enumerate(Inlist):
            if debug: print("{}*{:2d} + ".format(el, applyPattern[(i+1)%len(applyPattern)]), end='')
            digit += (int(el)*applyPattern[(i+1)%len(applyPattern)])
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

def hundertPhases(inlist):
    out = ''.join(map(str, phase(inlist, debug=False)))
    print('.', end='')
    for _ in range(99):
        out = ''.join(map(str, phase(out, debug=False)))
        print('.', end='')
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

def runPartTwo():
    print("run Part Two")
    print("############")


if __name__ == '__main__':
    run_small_test()
    runPartOne()
    run_small_test2()
    runPartTwo()