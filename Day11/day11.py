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



from itertools import defaultdict

class Painter:

    def __init__(self):
        self.direction = '^'
        self.position = [0,0]
        self.painted = defaultdict(int)

    def paint_black(self):
        self.painted[self.position] = 0

    def paint_white(self):
        self.painted[self.position] = 1
    
    def paint(self, color):
        self.painted[self.position] = color

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


def run_small_test():
    print("small Test 1")
    print("############")

def runPartOne():
    print("run Part One")
    print("############")

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