
import CheckParser
import re
import unittest
import itertools


class ParserIniPosTest(unittest.TestCase):
    def setUp(self):
        self.testObj = CheckParser.CheckParser(0)
        print("ParserIniPos SetUp executed")

    def tearDown(self):
        self.testObj = None
        print("ParserIniPos TearDown executed")

    def test_ini_pos(self):
        self.assertEqual(self.testObj.position, 0, "Initial position is not 0")

    def test_changed_pos(self):
        self.testObj.position = 1
        self.assertEqual(self.testObj.position, 1, "Initial position didn't change")

    def test_negative_pos(self):
        self.assertRaises(ValueError, CheckParser.CheckParser, -1)


class FileWriteReadTest(unittest.TestCase):
    def setUp(self):
        self.filename = r"C:\Users\nero_luci\Desktop\GitHub\CheckGuard\tests\pos.txt"
        print("FileWriteRead SetUp executed")

    def tearDown(self):
        print("FileWriteRead TearDown executed")

    def test_write_2_file(self):
        value_2_file = "0"
        CheckParser.write_init_pos(value_2_file)
        with open(self.filename, "r") as tf:
            expected = tf.read()
        self.assertEqual(expected, value_2_file, "File writing failed")

    def test_read_from_file(self):
        expected = 0
        read_value = CheckParser.read_init_pos()
        self.assertEqual(expected, read_value, "File reading failed")


class RegexTest(unittest.TestCase):
    def setUp(self):
        self.test_list_1 = ["2 x #2    mere pere  @ 0,01                0%  0,01",
                            "1 x #33    hubba bubba  @ 12,50                9%  0,01",
                            "7 x #103  Cappuccino  @ 7,00             24%  7,00",
                            "5 x #2400 Dorna Apa  @ 555,70              24%  5,70",
                            "3 x #307  Frappe  @ 7,50                   9% 7,50",
                            "25 x #101  Cafea  @ 5,50                  24%  11,00",
                            "2 x #2101 Bere  @ 6,70                   24%   13,40",
                            "66 x #2327 Lemonade  @ 6,00             0%     6,00",
                            "8 x #2310 Fresh  @ 8,80                  16%   8,80",
                            "999 x #2332 Whisky&Cola  @ 9,90               11%  19,80"
                            ]
        self.test_line_3 = "cnaldknpinda    %  @ xx \/'*&"
        self.prices = ['0,01', '12,50', '7,00', '555,70', '7,50', '5,50', '6,70', '6,00', '8,80', '9,90']
        self.qtys = ['2', '1', '7', '5', '3', '25', '2', '66', '8', '999']
        self.tvas = ['0%', '9%', '24%', '24%', '9%', '24%', '24%', '0%', '16%', '11%']
        self.names = ['mere pere', 'hubba bubba', 'Cappuccino', 'Dorna Apa', 'Frappe', 'Cafea', 'Bere',
                      'Lemonade', 'Fresh', 'Whisky&Cola']

    def tearDown(self):
        pass

    def test_price_regex_1(self):

        for line, price in itertools.izip(self.test_list_1, self.prices):
            reg_ex = re.search('\d+\,\d+', line)
            # self.assertIsNotNone(reg_ex, "Regex price is not valid: test 1")
            self.assertEqual(line[reg_ex.start():reg_ex.end()], price, "Price not equal")

    def test_qty_regex_1(self):
        for line, qty in itertools.izip(self.test_list_1, self.qtys):
            reg_ex = re.search('\d+', line)
            #self.assertIsNotNone(reg_ex, "Regex quantity is not valid: test 1")
            self.assertEqual(line[reg_ex.start():reg_ex.end()], qty, "Quantity not equal")

    def test_qty_regex_2(self):
        reg_ex = re.search('\d+', self.test_line_3)
        self.assertIsNone(reg_ex, "Regex quantity is not valid: test 3")

    def test_tva_regex_1(self):
        for line, tva in itertools.izip(self.test_list_1, self.tvas):
            reg_ex = re.search('\d{1,2}%', line)
            # self.assertIsNotNone(reg_ex, "Regex tva is not valid: test 1")
            self.assertEqual(line[reg_ex.start():reg_ex.end()], tva, "Tva not equal")

    def test_name_regex_1(self):
        for line, name in itertools.izip(self.test_list_1, self.names):
            reg_ex = re.search('[a-zA-Z]{2,}[\S\s]?[a-zA-Z]*[\S\s]?[a-zA-Z]*', line)
            # self.assertIsNotNone(reg_ex, "Regex name is not valid: test 1")
            self.assertEqual(line[reg_ex.start():reg_ex.end()].strip(' '), name, "Name not equal")


class ParserReadCheckFile(unittest.TestCase):
    """
    For this test you should comment 2 lines in CheckParser.py read_file():
    self.generate_new_check()
    self.check_data = []
    """
    def setUp(self):
        self.testObj = CheckParser.CheckParser(0, r"C:\Users\nero_luci\Desktop\GitHub\CheckGuard\tests\files.txt")
        self.testObj2 = CheckParser.CheckParser(0, r"C:\Users\nero_luci\Desktop\GitHub\CheckGuard\tests\files2.txt")
        self.expected_check_1 = ["1 x #2    bacsis  @ 0,01                0%  0,01  \r\n",
                                 "1 x #1    extra  @ 0,10                24%  0,10  \r\n"]
        self.expected_check_2 = []

    def test_data_1(self):
        self.testObj.read_file()
        self.assertListEqual(self.testObj.check_data, self.expected_check_1, "Lists are not equal: test 1")

    def test_data_2(self):
        self.testObj2.read_file()
        self.assertListEqual(self.testObj2.check_data, self.expected_check_2, "Lists are not equal: test 2")

testList = [ParserIniPosTest, FileWriteReadTest, RegexTest, ParserReadCheckFile]
testLoad = unittest.TestLoader()

caseList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    caseList.append(testSuite)

checkGuardTestSuite = unittest.TestSuite(caseList)
runner = unittest.TextTestRunner()
runner.run(checkGuardTestSuite)