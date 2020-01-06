import day16
import unittest


# 80871224585914546619083218645595 becomes 24176176.
# 19617804207202209144916044189917 becomes 73745418.
# 69317163492948606335995924319873 becomes 52432133.


class TestRunner(unittest.TestCase):
    
    def test_day16_1_1(self):
        Input = '80871224585914546619083218645595'
        expected = '24176176'
        out2 = day16.hundertPhases(day16.int2list(Input))
        out = ''.join(map(str, out2))
        self.assertEqual(out, expected)

    def test_day16_1_2(self):
        Input = '19617804207202209144916044189917'
        expected = '73745418'
        out2 = day16.hundertPhases(day16.int2list(Input))
        out = ''.join(map(str, out2))
        self.assertEqual(out, expected)

    def test_day16_1_3(self):
        Input = '69317163492948606335995924319873'
        expected = '52432133'
        out2 = day16.hundertPhases(day16.int2list(Input))
        out = ''.join(map(str, out2))
        self.assertEqual(out, expected)

    def test_day16_1_4(self):
        Input = '12345678'

        expected = '48226158'
        out2 = day16.phase(day16.int2list(Input))
        out = ''.join(map(str, out2))
        self.assertEqual(out, expected)
        
        expected = '34040438'
        out2 = day16.phase(day16.int2list(out))
        out = ''.join(map(str, out2))

        expected ='03415518'
        out2 = day16.phase(day16.int2list(out))
        out = ''.join(map(str, out2))

        expected = '01029498'
        out2 = day16.phase(day16.int2list(out))
        out = ''.join(map(str, out2))


if __name__ == '__main__':
    unittest.main()
