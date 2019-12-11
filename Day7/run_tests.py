import day7
import unittest
import io
import re

from unittest.mock import patch

progA = """3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"""
progB = """3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"""
progC = """3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"""


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

    def test_day7_1_1(self):
        self.assertEqual(day7.runCode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_day7_1_2(self):
        self.assertEqual(day7.runCode([1,0,0,0,99]), [2,0,0,0,99])
    
    def test_day7_1_3(self):
        self.assertEqual(day7.runCode([2,3,0,3,99]), [2,3,0,6,99])

    def test_day7_1_4(self):
        self.assertEqual(day7.runCode([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_day7_1_5(self):
        self.assertEqual(day7.runCode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_day7_1_6(self):
        self.assertEqual(day7.runCode([1002,4,3,4,33]), [1002,4,3,4,99])

    def test_day7_1_7(self):
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

    def test_day7_1_1(self):
        maxThrust, phaseSeq = day7.optimize(progA)
        self.assertEqual(maxThrust, 43210)
        self.assertEqual(phaseSeq, [4,3,2,1,0])
    
    def test_day7_1_2(self):
        maxThrust, phaseSeq = day7.optimize(progB)
        self.assertEqual(maxThrust, 54321)
        self.assertEqual(phaseSeq, [0,1,2,3,4])
    
    def test_day7_1_3(self):
        maxThrust, phaseSeq = day7.optimize(progC)
        self.assertEqual(maxThrust, 65210)
        self.assertEqual(phaseSeq, [1,0,4,3,2])
    
    # def test_day6_2_1(self):
    #     self.assertEqual(day6.getNumberOfTransfers("test_input_2"), 4)


if __name__ == '__main__':
    unittest.main()