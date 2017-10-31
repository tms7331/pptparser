import itertools
import re
import numpy as np
import os
import time


import SyntaxValidator as sv

import unittest
import RangeParserMasks as rp

import UnitTests_TestDicts as td


class testRangeParserMasks(unittest.TestCase):

    def testRanges(self):


        types_list = [td.basicHandsPlain, td.basicHandsVars, td.basicHandsBrackets]
        test_list = [td.basicHands1, td.basicHands2, td.basicHands3]
        macros_list = [td.macros1, td.macros2, td.macros3]
        long_list = [td.dictOne, td.dictTwo, td.dictThree, td.dictFour, td.dictFive, td.dictSix, td.dictSeven, td.dictEight]
        
        all_list = types_list+test_list+macros_list+long_list

        for testDict in long_list:

            for myKey in testDict:

                rangeCards,rangeMask = rp.evaluate(myKey)
                self.assertTrue(len(rangeCards)==testDict[myKey],msg="Range mismatch {} {} {}".format(myKey,len(rangeCards),testDict[myKey]))


tester = testRangeParserMasks()
tester.testRanges()

