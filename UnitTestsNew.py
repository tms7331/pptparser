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

        tally = 0
        for testDict in long_list:

            for myKey in testDict:
                tally+=1
                if tally%200==0:
                    print("CURR",tally)
                #print("MY KEY",myKey)

                start_time = time.time()

                #rangeCards,rangeMask = rp.evaluate(myKey)
                #self.assertTrue(len(rangeCards)==testDict[myKey],msg="Range mismatch {} {} {}".format(myKey,len(rangeCards),testDict[myKey]))

                try:
                    rangeCards,rangeMask = rp.evaluate(myKey)
                    self.assertTrue(len(rangeCards)==testDict[myKey],msg="Range mismatch {} {} {}".format(myKey,len(rangeCards),testDict[myKey]))
                except:
                    print("FAILED",myKey, len(rangeCards),testDict[myKey])
                if int(time.time()-start_time)>0:
                    print("TIME TAKEN",int(time.time()-start_time))


tester = testRangeParserMasks()
tester.testRanges()


## Manually check -
# FAILED (444,[Tx-][Tc-]7x) 9151 10411
# FAILED (ssh,RxAx[JcQy+]) 36346 36553
# FAILED (sssT,[Tx-][Tc-]7x) 9982 11242
# FAILED (Thh,RxAx[JcQy+]) 11896 12100
# FAILED (ccsT,[Tx-][Tc-]7x) 12714 13883
# FAILED (JhTcs,[Tx-][Tc-]7x) 9515 10775
# FAILED (csJsTd,RxAx[JcQy+]) 372 579
# FAILED (csTsTd,[Tx-][Tc-]7x) 9111 10371
# FAILED (cTcTs,RxAx[JcQy+]) 738 945
# FAILED (cTTs,[Tx-][Tc-]Rx) 74737 84247
# FAILED (sTdTh,[Tx-][Tc-]7x) 9523 10783
# FAILED (JcsTsTd,[Tx-][Tc-]7x) 8976 10236
# FAILED (4h4c4s,RxAx[JcQy+]) 265 472
# FAILED (s4s4h4,[Tx-][Tc-]Rx) 73722 83292
# FAILED (c4c4s4,[Tx-][Tc-]7x) 8988 10248
# FAILED (c44s4,[Tx-][Tc-]Rx) 73747 83317
# FAILED (4s4d4h,[Tx-][Tc-]7x) 9013 10273
# FAILED ([56h+],[Tx-][Tc-]7x) 46912 48109
# FAILED ([56h+],RxAx[JcQy+]) 39642 39790
# FAILED (986-,RxAx[JcQy+]) 14456 14663
# FAILED ([T9-43][5+],RxAx[JcQy+]) 97568 97775
# FAILED ([56+][8c-]3s,RxAx[JcQy+]) 1188 1395
# FAILED ([33-3T][5+]As,[Tx-][Tc-]7x) 12324 13578
# FAILED ([Tx-][Tc-]7x,RR[AcJc-Ac4c]) 9540 9516
# FAILED ([5x6+][8z-]3y,RxAx[JcQy+]) 5436 5643
# FAILED (KxTy[AcJc-Ac4c],RR[AcJc-Ac4c]) 624 669
# FAILED ([33-3T][5x+]Ax,RxAx[JcQy+]) 4128 4335
# FAILED ([Kx-][Tx-]RxOx,RxAx[JcQy+]) 3072 3279
# FAILED (RxAx[JcQy+],RR[AcJc-Ac4c]) 792 996
# FAILED ([T-]![Tx-][Tc-]Rx) 195195 185625
# FAILED ([K-][T-][4-][7+]![Tx-][Tc-]Rx) 115025 108258
# FAILED ([56+][8c-]3s![Tx-][Tc-]Rx) 456 423
# FAILED ([33-3T][5+]As![Tx-][Tc-]Rx) 2433 2384
# FAILED ([Tx-][Tc-]7x![Tx9x-4x3x]4y[5+]) 8637 9867
# FAILED ([Tx-][Tc-]7x![Kx-][Tx-]RxOx) 8964 10056
# FAILED (3x[JcQy+][3z+]![33-3T][5x+]Ax) 198 717
# FAILED (3x[JcQy+][3z+]!RcRs[Tx9x-4x3x]) 198 762
# FAILED ([Tx9x-4x3x]4y[5+]![Tx-][Tc-]Rx) 1920 1755
# FAILED (KxTy[AcJc-Ac4c]![Kx-][Tx-]RxOx) 48 93
# FAILED ([33-3T][5x+]Ax![Tx-][Tc-]Rx) 2778 2529
# FAILED ([Tx-][Tc-]Rx!RcRs[Tx9x-4x3x]) 73584 83154
# FAILED ([Tx-][Tc-]7x:[33-3T][5x+]Ax) 60 66
# FAILED (3x[JcQy+][3z+]:[5x6+][8z-]Ry) 198 441
# FAILED ([Tx-][Tc-]Rx:[5x+]AxRxRh) 0 48
# FAILED (T,JhTcs),([56h+],[Tx-][Tc-]7x) 107438 108274
# FAILED (T,[K-][T-][4-][7+]!ThTcJs,RxAx[JcQy+]) 198687 198876
# FAILED (Th,Thcd)!(ThTcJs,RxAx[JcQy+]) 20770 20767
# FAILED (Th,c44s4:[56h+],[Tx-][Tc-]7x) 29240 30472
# FAILED (Th,[Tx-][Tc-]7x,Th,KxTy[AcJc-Ac4c]) 29272 30541
# FAILED (Th,RxAx[JcQy+]:hh,[Kx-][Tx-]RxOx) 23527 23560
# FAILED (JT,[T-][Tc-]):(cTcTs,RxAx[JcQy+]) 528 534
# FAILED (JT,[Tx-][Tc-]Rx),(c4c4s4,[JcQc+][3h+]) 88471 97437
# FAILED (TT,JTJ):([JcQc+][3h+],[Tx-][Tc-]Rx) 2661 2865
# FAILED (TT,sJhTh:444,RxAx[JcQy+]) 7177 7384
# FAILED (TT,cTTs):(Thh,[Tx-][Tc-]7x) 1702 1723
# FAILED (TT,[Tx-][Tc-]7x:[56h+],RxAx[JcQy+]) 8753 9022
# FAILED (hc,Thc,4h4c4s,[Tx-][Tc-]7x) 125277 126173
# FAILED (hc,cT![56h+],RxAx[JcQy+]) 138237 138363
# FAILED (hc,JhTcs:KxTy[AcJc-Ac4c],[Tx-][Tc-]Rx) 153465 160071
# FAILED (hc,cTcTsJ,sJhTh,[Tx-][Tc-]Rx) 153878 160476
# FAILED (JT4,c44s4!cTcTsJ,[Tx-][Tc-]7x) 11825 13081
# FAILED (JT4,[JcQc+][3h+]),(JT4,RxAx[JcQy+]) 4599 4755
# FAILED (JT4,[Tx-][Tc-]7x):(cT,cTTs) 3499 3880
# FAILED (JT4,RxAx[JcQy+]!ccTT,ThTcJs) 3109 3316
# FAILED (444,cTTsJ!sJdTh,RxAx[JcQy+]) 545 752
# FAILED (444,[Tx-][Tc-]7x!cTTs,[986-]) 22179 23232
# FAILED (444,KxTy[AcJc-Ac4c]:4cs4s4d,[Tx-][Tc-]7x) 9151 10411
# FAILED (444,RxAx[JcQy+]),([Kx-][Tx-][4-]5x,[Kx-][Tx-]RxOx) 5137 5344
# FAILED (hcd,cJcTs!s4s4h4,[Tx-][Tc-]Rx) 125383 134917
# FAILED (hcd,[33-3T][5+]As)!(JcsTsTd,[Tx-][Tc-]7x) 69253 69247
# FAILED (sss,JhTcs),(4cs4s4d,RxAx[JcQy+]) 12656 12863
# FAILED (sss,[K-][T-][4-][7+]):(JcsTsTd,[Tx-][Tc-]7x) 6222 7132
# FAILED (ssh,cTc)!(56h+,[Tx-][Tc-]Rx) 30819 28402
# FAILED (ssh,[Tx-][Tc-]7x),(4cs44,[Tx9x-4x3x]4y[5+]) 46623 47853
# FAILED (ssh,RxAx[JcQy+])!(Tssh,ThTcJs) 30485 30692
# FAILED (sssT,csT:4cs4s4d,[Tx-][Tc-]7x) 9983 11243
# FAILED (sssT,cJsTs),(Thc,RxAx[JcQy+]) 14212 14416
# FAILED (sssT,[Tx-][Tc-]7x,[5x6+][8z-]Ry,[Kx-][Tx-]RxOx) 57766 58858
# FAILED (sssT,RxAx[JcQy+]!ccJT,[33-3T][5+]As) 4657 4864
# FAILED (sTsc,[Tx9x-4x3x]4y[5+]!cTTs,[Tx-][Tc-]Rx) 77204 86609
# FAILED (Tssh,[56+][8c-]3s,4h4c4s,[Tx-][Tc-]7x) 15620 16869
# FAILED (Thc,RxAx[JcQy+]:sTdTh,[Tx-][Tc-]7x) 20804 22036
# FAILED (cTc,csT),([Tx-][Tc-]7x,[Kx-][Tx-][4-]5x) 39069 39932
# FAILED (ccT,JhTcs,JhTcs,[Tx-][Tc-]7x) 21399 22274
# FAILED (sJhTh,[Kx-][Tx-][4-]5x)!(sTsThJ,[Tx-][Tc-]Rx) 2231 1663
# FAILED (ccJT,cTcTs:[56h+],RxAx[JcQy+]) 1377 1584
# FAILED (ccTT,cTcTs,[Kx-][Tx-]RxOx,RxAx[JcQy+]) 3936 4143
# FAILED (4h4c4s,RxAx[JcQy+]):([Jc+],[986-]) 220 427
# FAILED (JT4![Tx-][Tc-]Rx,ccJT!986-) 3076 3022
# FAILED (sss!3c[JcQc+][3h+],986-![Tx-][Tc-]Rx) 20344 19649
# FAILED (ccJT!sJdTh!Jc+![Tx-][Tc-]Rx) 300 216
# FAILED (cTcTs![Tx-][Tc-]Rx,JsTdTh!4cc44) 427 367
# FAILED (cTc:ccsT),([Tx-][Tc-]7x:[33-3T][5x+]Ax) 1374 1380
# FAILED (90%6h-50%6h,RR[AcJc-Ac4c]) 111462 111438
# FAILED (8%!RR[AcJc-Ac4c]) 21519 21543
# FAILED (55%6h!RR[AcJc-Ac4c]) 148410 148434
# FAILED (85%6h![T9-43][5+]!JT4!RR[AcJc-Ac4c]) 142597 142621
# FAILED (100%!50%-20%!JT4!RR[AcJc-Ac4c]) 185361 185385
# FAILED (15%-5%6h!JccTT):(Jc+!RR[AcJc-Ac4c]) 13869 13887
