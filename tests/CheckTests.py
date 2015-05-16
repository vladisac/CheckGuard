__author__ = 'nero_luci'


import CheckParser
import unittest


class ParserIniPosTest(unittest.TestCase):
    def setUp(self):
        self.testObj = CheckParser.CheckParser(0)
        print("SetUp executed")

    def tearDown(self):
        self.testObj = None
        print("TearDown executed")

    def test_ini_pos(self):
        self.assertEqual(self.testObj.position, 0, "Initial position is not 0")

    def test_changed_pos(self):
        self.testObj.position = 1
        self.assertEqual(self.testObj.position, 1, "Initial position didn't change")

    def test_negative_pos(self):
        self.assertRaises(ValueError, CheckParser.CheckParser, -1)


testList = [ParserIniPosTest]
testLoad = unittest.TestLoader()

caseList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    caseList.append(testSuite)

checkGuardTestSuite = unittest.TestSuite(caseList)
runner = unittest.TextTestRunner()
runner.run(checkGuardTestSuite)