import day11
import unittest

class TestRunner(unittest.TestCase):
    
    def test_aa_run_1(self):
        _in = 7
        _exp = 999
        _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        amp = day11.Computer(_prog)
        amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)
    
    def test_aa_run_2(self):
        _in = 8
        _exp = 1000
        _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        amp = day11.Computer(_prog)
        amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)

    def test_aa_run_3(self):
        _in = 9
        _exp = 1001
        _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        amp = day11.Computer(_prog)
        amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)

    def test_aa_run_4(self):
        _prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        amp = day11.Computer(_prog)
        _out = amp.run(debug=False)
        self.assertEqual(_out, _prog)

    def test_aa_run_5(self):
        _prog = [1102,34915192,34915192,7,4,7,99,0]
        amp = day11.Computer(_prog)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(len(str(_out)), 16)

    def test_aa_run_6(self):
        #_in = 9
        _exp = 1125899906842624
        _prog = [104,1125899906842624,99]
        amp = day11.Computer(_prog)
        #amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)

    def test_day11_1_1(self):
        self.assertEqual(8, 8)

if __name__ == '__main__':
    unittest.main()
