# day4

def hasDouble(pw):
    for i in range(len(pw)-1):
        if pw[i] == pw[i+1]:
            return True
    return False

def Decreases(pw):
    for i in range(len(pw)-1):
        if pw[i+1] < pw[i]:
            return True
    return False

def isValidPassword(_pw):
    pw = str(_pw)
    if len(pw) is not 6:
        return False
    if not hasDouble(pw):
        return False
    if Decreases(pw):
        return False
    return True

def hasSpecialDouble(pw):
    return True

def runPartOne(minimum = 168630, maximum = 718098):
    pws = []
    for i in range(minimum, maximum+1):
        # print(".".format(i), end='')
        if isValidPassword(i):
            pws.append(i)
    print()
    print(pws)
    print(len(pws))

def runPartTwo(minimum = 168630, maximum = 718098):
    pws = []
    for i in range(minimum, maximum+1):
        if isValidPassword(i):
            if hasSpecialDouble(i):
                pws.append(i)
    print()
    print(pws)
    print(len(pws))

if __name__ == '__main__':
    runPartOne()
    runPartTwo()