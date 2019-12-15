# day8

class Layer():
    rows = []

    def __init__(self, _rows):
        self.rows = _rows

    def getFlatList(self):
        return [item for sublist in self.rows for item in sublist]

    def print(self):
        #print(self.rows)
        for row in self.rows:
            print("  ", end='')
            print(*row)


class Image():
    layers    = []
    N_rows    = 0
    N_columns = 0
    N_layers  = 0
    _data = []

    def __init__(self, __data, _N_columns, _N_rows):
        self.N_rows    = _N_rows
        self.N_columns = _N_columns
        self.layers    = []
        tmpRow   = []
        tmpLayer = []
        self._data = __data[:]
        for idx, el in enumerate(self._data):
            #print ("{}: {}     {}     {}".format(idx, el, idx % self.N_columns, idx % (self.N_rows*self.N_columns)))
            if idx % self.N_columns == 0 and idx != 0:
                # row is full
                tmpLayer.append(tmpRow)
                tmpRow = []
            if idx % (self.N_rows*self.N_columns) == 0 and idx != 0:
                # layer is full
                self.layers.append(Layer(tmpLayer))
                tmpLayer = []
                tmpRow = []
            tmpRow.append(int(el))
        # last thing has to be added manually 
        tmpLayer.append(tmpRow)
        self.layers.append(Layer(tmpLayer))
        self.N_layers = len(self.layers)

    def getCountOfNumberInLayer(self, number, layerId):
        out = 0
        flatList = self.layers[layerId].getFlatList() 
        #print(flatList)
        for el in flatList:
            if el == number:
                out += 1
        return out

    def getCountOfNumber(self, number):
        out = []
        for layerId in range(self.N_layers):
            tmp = self.getCountOfNumberInLayer(number, layerId)
            out.append([layerId, tmp])
        return out

    def print(self):
        i = 1
        for layer in self.layers:
            print("Layer {}:\n~~~~~~~~~~~~~~~~~~".format(i))
            layer.print()
            i += 1

class FlattendImage(Layer):
    rows = []

    def __init__(self, _image):
        image = _image
        self.rows = image.layers[0].rows[:]
        self.print()
        layerId = 1
        while layerId < len(image.layers):
            print(layerId)
            for idr, row in enumerate(image.layers[layerId].rows):
                for idc, belowPixel in enumerate(row):
                    abovePixel = self.rows[idr][idc]
                    if abovePixel == 2:
                        self.rows[idr][idc] = belowPixel
            layerId += 1

    def nice(self):
        for row in self.rows:
            for el in row:
                if el == 0:
                    a = ' '
                elif el == 1:
                    a = '#'
                else:
                    raise TypeError
                print(a, end='')
            print()




def run_small_test():
    data__ = "123456789012"
    image__ = Image(data__, 3, 2)
    image__.print()

def loadInput(fname='input'):
    with open(fname, 'r') as f:
        a = f.read()
    return a

def runPartOne():
    inp1 = loadInput()
    image_1 = Image(inp1, 25, 6)
    zeroes = image_1.getCountOfNumber(0)
    print(zeroes)
    layerID_min_zero = min(zeroes, key=lambda x: x[1])[0]
    image_1.layers[layerID_min_zero].print()
    print(layerID_min_zero)
    result = image_1.getCountOfNumberInLayer(1, layerID_min_zero) * image_1.getCountOfNumberInLayer(2, layerID_min_zero)
    print(result)

def runSmall2():
    inp = "0222112222120000"
    image_test = Image(inp, 2, 2)
    flat_test = FlattendImage(image_test)
    flat_test.print()
    flat_test.nice()

def runPartTwo():
    inp = loadInput()
    image_2 = Image(inp, 25, 6)
    #image_2.print()
    flat_2 = FlattendImage(image_2)
    flat_2.print()
    flat_2.nice()


if __name__ == '__main__':
    print("test1")
    print("************")
    run_small_test()
    print("Part1")
    print("************")
    runPartOne()
    print("test2")
    print("************")
    runSmall2()
    print("Part2")
    print("************")
    runPartTwo()