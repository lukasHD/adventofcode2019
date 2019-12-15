import day7
import unittest
import io
import re

from unittest.mock import patch

progA = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
progB = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
progC = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
progD = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
progE = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]


class TestRunner(unittest.TestCase):
    
    def test_day2_1_1(self):
        self.assertEqual(day7.runCode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_day2_1_2(self):
        self.assertEqual(day7.runCode([1,0,0,0,99]), [2,0,0,0,99])
    
    def test_day2_1_3(self):
        self.assertEqual(day7.runCode([2,3,0,3,99]), [2,3,0,6,99])

    def test_day2_1_4(self):
        self.assertEqual(day7.runCode([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_day2_1_5(self):
        self.assertEqual(day7.runCode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_day5_1_1(self):
        self.assertEqual(day7.runCode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_day5_1_2(self):
        self.assertEqual(day7.runCode([1,0,0,0,99]), [2,0,0,0,99])
    
    def test_day5_1_3(self):
        self.assertEqual(day7.runCode([2,3,0,3,99]), [2,3,0,6,99])

    def test_day5_1_4(self):
        self.assertEqual(day7.runCode([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_day5_1_5(self):
        self.assertEqual(day7.runCode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_day5_1_6(self):
        self.assertEqual(day7.runCode([1002,4,3,4,33]), [1002,4,3,4,99])

    def test_day5_1_7(self):
        self.assertEqual(day7.runCode([1101,100,-1,4,0]), [1101,100,-1,4,99])


    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_inp_1(self, input, mock_stdout):
        input.return_value = input_data = "123"

        day7.runCode([3,0,4,0,99])

        #print(mock_stdout.getvalue())
        regex = r"Output is: (\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)

        self.assertEqual(matches[-1], input_data)

    def getLastOutput(self, string, nothing):
        regex = r"Output is: (\d+)"
        matches = re.findall(regex, string, re.MULTILINE)
        return matches[-1]

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_inp_2(self, input, mock_stdout):
        input.return_value = input_data = "-456"
        
        day7.runCode([3,0,4,0,99])

        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)

        self.assertEqual(matches[-1], input_data)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_eql_1(self, input, mock_stdout):
        input.return_value = "8"
        expected = "1"

        day7.runCode([3,9,8,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_eql_2(self, input, mock_stdout):
        input.return_value = "7"
        expected = "0"

        day7.runCode([3,9,8,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_eql_3(self, input, mock_stdout):
        input.return_value = "-9"
        expected = "0"

        day7.runCode([3,9,8,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

# immediate mode
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_eql_4(self, input, mock_stdout):
        input.return_value = "8"
        expected = "1"

        day7.runCode([3,3,1108,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_eql_5(self, input, mock_stdout):
        input.return_value = "7"
        expected = "0"

        day7.runCode([3,3,1108,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_eql_6(self, input, mock_stdout):
        input.return_value = "-9"
        expected = "0"

        day7.runCode([3,3,1108,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)


    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_les_1(self, input, mock_stdout):
        input.return_value = "7"
        expected = "1"

        day7.runCode([3,9,7,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_les_2(self, input, mock_stdout):
        input.return_value = "8"
        expected = "0"

        day7.runCode([3,9,7,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_les_3(self, input, mock_stdout):
        input.return_value = "9"
        expected = "0"

        day7.runCode([3,9,7,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

# immediate mode 
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_les_4(self, input, mock_stdout):
        input.return_value =  "7"
        expected = "1"

        day7.runCode([3,3,1107,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_les_5(self, input, mock_stdout):
        input.return_value = "8"
        expected = "0"

        day7.runCode([3,3,1107,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_les_6(self, input, mock_stdout):
        input.return_value = "9"
        expected = "0"

        day7.runCode([3,3,1107,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_jmp_1(self, input, mock_stdout):
        input.return_value = "0"
        expected = "0"

        day7.runCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_jmp_2(self, input, mock_stdout):
        input.return_value = "-100"
        expected = "1"

        day7.runCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_jmp_3(self, input, mock_stdout):
        input.return_value = "123"
        expected = "1"

        day7.runCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    # immediate mode
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_jmp_4(self, input, mock_stdout):
        input.return_value = "0"
        expected = "0"

        day7.runCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_jmp_5(self, input, mock_stdout):
        input.return_value = "-100"
        expected = "1"

        day7.runCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_jmp_6(self, input, mock_stdout):
        input.return_value = "123"
        expected = "1"

        day7.runCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    # test complex
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_run_1(self, input, mock_stdout):
        input.return_value = "7"
        expected = "999"

        day7.runCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_run_2(self, input, mock_stdout):
        input.return_value = "8"
        expected = "1000"

        day7.runCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day7, "input", create=True)
    def test_run_3(self, input, mock_stdout):
        input.return_value = "9"
        expected = "1001"

        day7.runCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    def test_z_day7_1_1(self):
        maxThrust, phaseSeq = day7.optimize(progA)
        self.assertEqual(maxThrust, 43210)
        self.assertEqual(phaseSeq, [4,3,2,1,0])
    
    def test_z_day7_1_2(self):
        maxThrust, phaseSeq = day7.optimize(progB)
        self.assertEqual(maxThrust, 54321)
        self.assertEqual(phaseSeq, [0,1,2,3,4])

    def test_z_day7_1_3(self):
        maxThrust, phaseSeq = day7.optimize(progC)
        self.assertEqual(maxThrust, 65210)
        self.assertEqual(phaseSeq, [1,0,4,3,2])

    def test_zz_run_1(self):
        _in = 7
        _exp = 999
        _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        amp = day7.Amp(_prog)
        amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)
    
    def test_zz_run_2(self):
        _in = 8
        _exp = 1000
        _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        amp = day7.Amp(_prog)
        amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)

    def test_zz_run_3(self):
        _in = 9
        _exp = 1001
        _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        amp = day7.Amp(_prog)
        amp.inp.put(_in)
        _out = amp.run(debug=False)[-1]
        self.assertEqual(_out, _exp)
    
    def test_zzz_day7_2_1(self):
        maxThrust, phaseSeq = day7.optimize2(progD)
        self.assertEqual(maxThrust, 139629729)
        self.assertEqual(phaseSeq, [9,8,7,6,5])

    def test_zzz_day7_2_2(self):
        maxThrust, phaseSeq = day7.optimize2(progE)
        self.assertEqual(maxThrust, 18216)
        self.assertEqual(phaseSeq, [9,7,8,5,6])


if __name__ == '__main__':
    unittest.main()