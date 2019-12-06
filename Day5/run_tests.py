import day5
import unittest
import io
import re

from unittest.mock import patch

# run tests like this `python -m unittest day1.py -v`


class TestRunner(unittest.TestCase):
    
    def test_day2_1_1(self):
        self.assertEqual(day5.runIntcode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_day2_1_2(self):
        self.assertEqual(day5.runIntcode([1,0,0,0,99]), [2,0,0,0,99])
    
    def test_day2_1_3(self):
        self.assertEqual(day5.runIntcode([2,3,0,3,99]), [2,3,0,6,99])

    def test_day2_1_4(self):
        self.assertEqual(day5.runIntcode([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_day2_1_5(self):
        self.assertEqual(day5.runIntcode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_day5_1_1(self):
        self.assertEqual(day5.runCode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_day5_1_2(self):
        self.assertEqual(day5.runCode([1,0,0,0,99]), [2,0,0,0,99])
    
    def test_day5_1_3(self):
        self.assertEqual(day5.runCode([2,3,0,3,99]), [2,3,0,6,99])

    def test_day5_1_4(self):
        self.assertEqual(day5.runCode([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_day5_1_5(self):
        self.assertEqual(day5.runCode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_day5_1_6(self):
        self.assertEqual(day5.runCode([1002,4,3,4,33]), [1002,4,3,4,99])

    def test_day5_1_7(self):
        self.assertEqual(day5.runCode([1101,100,-1,4,0]), [1101,100,-1,4,99])


    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_inp_1(self, input, mock_stdout):
        input.return_value = input_data = "123"
        expected = int(input_data)

        actual = day5.runCode([3,0,4,0,99])

        #print(mock_stdout.getvalue())
        regex = r"Output is: (\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)

        self.assertEqual(matches[-1], input_data)

    def getLastOutput(string, nothing):
        regex = r"Output is: (\d+)"
        matches = re.findall(regex, string, re.MULTILINE)
        return matches[-1]

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_inp_2(self, input, mock_stdout):
        input.return_value = input_data = "-456"
        expected = int(input_data)

        actual = day5.runCode([3,0,4,0,99])

        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)

        self.assertEqual(matches[-1], input_data)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_eql_1(self, input, mock_stdout):
        input.return_value = input_data = "8"
        expected = "1"

        actual = day5.runCode([3,9,8,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_eql_2(self, input, mock_stdout):
        input.return_value = input_data = "7"
        expected = "0"

        actual = day5.runCode([3,9,8,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_eql_3(self, input, mock_stdout):
        input.return_value = input_data = "-9"
        expected = "0"

        actual = day5.runCode([3,9,8,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

# immediate mode
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_eql_4(self, input, mock_stdout):
        input.return_value = input_data = "8"
        expected = "1"

        actual = day5.runCode([3,3,1108,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_eql_5(self, input, mock_stdout):
        input.return_value = input_data = "7"
        expected = "0"

        actual = day5.runCode([3,3,1108,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_eql_6(self, input, mock_stdout):
        input.return_value = input_data = "-9"
        expected = "0"

        actual = day5.runCode([3,3,1108,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)


    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_les_1(self, input, mock_stdout):
        input.return_value = input_data = "7"
        expected = "1"

        actual = day5.runCode([3,9,7,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_les_2(self, input, mock_stdout):
        input.return_value = input_data = "8"
        expected = "0"

        actual = day5.runCode([3,9,7,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_les_3(self, input, mock_stdout):
        input.return_value = input_data = "9"
        expected = "0"

        actual = day5.runCode([3,9,7,9,10,9,4,9,99,-1,8])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

# immediate mode 
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_les_4(self, input, mock_stdout):
        input.return_value = input_data = "7"
        expected = "1"

        actual = day5.runCode([3,3,1107,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_les_5(self, input, mock_stdout):
        input.return_value = input_data = "8"
        expected = "0"

        actual = day5.runCode([3,3,1107,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_les_6(self, input, mock_stdout):
        input.return_value = input_data = "9"
        expected = "0"

        actual = day5.runCode([3,3,1107,-1,8,3,4,3,99])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_jmp_1(self, input, mock_stdout):
        input.return_value = input_data = "0"
        expected = "0"

        actual = day5.runCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_jmp_2(self, input, mock_stdout):
        input.return_value = input_data = "-100"
        expected = "1"

        actual = day5.runCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_jmp_3(self, input, mock_stdout):
        input.return_value = input_data = "123"
        expected = "1"

        actual = day5.runCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    # immediate mode
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_jmp_4(self, input, mock_stdout):
        input.return_value = input_data = "0"
        expected = "0"

        actual = day5.runCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_jmp_5(self, input, mock_stdout):
        input.return_value = input_data = "-100"
        expected = "1"

        actual = day5.runCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_jmp_6(self, input, mock_stdout):
        input.return_value = input_data = "123"
        expected = "1"

        actual = day5.runCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        regex = r"Output is: (-*\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)
        self.assertEqual(matches[-1], expected)

if __name__ == '__main__':
    unittest.main()