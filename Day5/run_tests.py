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

    #def setUp(self):
    #    # input is untouched before test
    #    assert day5.input is builtins.input

    #def test_day5_1_mockInput(self):
    #    day5.runCode([3,0,4,0,99])
    #    self.assertEqual(1,1)

    #def test_using_with(self):
    #    input_data = "123"
    #    expected = int(input_data)

    #    with patch.object(day5, "input", create=True, 
    #            return_value=expected):
    #        # create=True is needed as input is not in the globals of 
    #        # day5, but actually found in builtins .
    #        actual = day5.runCode([3,0,4,0,99])

    #    self.assertEqual(expected, actual)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(day5, "input", create=True)
    def test_using_decorator(self, input, mock_stdout):
        input.return_value = input_data = "123"
        expected = int(input_data)

        actual = day5.runCode([3,0,4,0,99])

        #print(mock_stdout.getvalue())
        regex = r"Output is: (\d+)"
        matches = re.findall(regex, mock_stdout.getvalue(), re.MULTILINE)

        self.assertEqual(matches[-1], input_data)


    #def tearDown(self):
    #    # raw input is restored aftest
    #    assert day5.input is builtins.input



if __name__ == '__main__':
    unittest.main()