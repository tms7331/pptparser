import itertools
import re
import numpy as np
import os


import SyntaxValidator as sv

#ploDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#ploDir = ploDir + '/solver/'
#retFile = np.load(ploDir+'npfiles/pptRankedHUnums.npy')

import unittest
import RangeParserMasks as rp
from UnitTests_RangeParserMasksTestDict import dictOne,dictTwo,dictThree,dictFour,dictFive,dictSix,dictSeven,dictEight,paradigmDictUnderlying,paradigmDictCopies,dictMacros

class testRangeParserMasks(unittest.TestCase):

    def testRanges(self):
        '''
        So here code is an absolute mess, but as long as it's working don't
        really want to mess with it too much.  Currently not fully working
        though.

        So with PQL we can return wins/losses/ties it seems?
        So we could use those to get equity counts?
        '''

        #Again, want to generate a bunch of random ranges
        #Test the combo counts to what we get back in PPT


        # There's the basic range matching, and then there's
        # the part that combines them together.

        # We can test them separately


        #So test a bunch of individual ranges
        #probably do each one to be safe, ppt lookups of all the masks
        #And then test the ,()!: with fake ranges.  Ultimately it's just masks?



        #rangeCards,rangeMask = rp.evaluate('(90%6h-50%6h!JT4)!([K-][T-][4-]5![Kx-][Tx-]RxOx)')
        #print("First")
        #rangeCards,rangeMask = rp.evaluate('(90%6h-50%6h!JT4)')
        #print(len(rangeCards))
        #print("Second")
        #rangeCards,rangeMask = rp.evaluate('[K-][T-][4-]5')
        #print(len(rangeCards))
        #print("Third")
        #rangeCards,rangeMask = rp.evaluate('[5c-][4c-]RxRy')


        #rangeCards,rangeMask = rp.evaluate('(90%6h-50%6h!JT4)!([K-][T-][4-]5![Kx-][Tx-]RxOx)')
        #rangeCards,rangeMask = rp.evaluate('(90%6h-50%6h!JT4)!([K-][T-][4-]5![Kx-][Tx-]RxOx)')

        #'([Tx-][Tc-]7x,RR[AcJc-Ac4c])',
        failList = [None
        ]
        '''
        for board in failList:
            print(board)
            rangeCards,rangeMask = rp.evaluate(board)

            if board in dictFive:
                self.assertTrue(len(rangeCards)==dictFive[board],msg="Range mismatch {} {} {}".format(board,len(rangeCards),dictFive[board]))

            elif board in dictSix:
                self.assertTrue(len(rangeCards)==dictSix[board],msg="Range mismatch {} {} {}".format(board,len(rangeCards),dictSix[board]))

            elif board in dictSeven:
                self.assertTrue(len(rangeCards)==dictSeven[board],msg="Range mismatch {} {} {}".format(board,len(rangeCards),dictSeven[board]))

            elif board in dictEight:
                self.assertTrue(len(rangeCards)==dictEight[board],msg="Range mismatch {} {} {}".format(board,len(rangeCards),dictEight[board]))

            else:
                print("BOARD NOT FOUND",board)
        '''

        totalTrials = 5
        
        for testDict in [dictFive,dictSix,dictSeven,dictEight]:  #[dictOne,dictTwo,dictThree,dictFour]:# ,dictFive,dictSix]:
            print("TestDict",[dictFive,dictSix,dictSeven,dictEight].index(testDict))

            localTrials = 0

            for myKey in testDict:
                print("MY KEY",myKey)
                localTrials+=1

                try:
                    rangeCards,rangeMask = rp.evaluate(myKey)
                    self.assertTrue(len(rangeCards)==testDict[myKey],msg="Range mismatch {} {} {}".format(myKey,len(rangeCards),testDict[myKey]))
                except:
                    print("Failed on",myKey)
                    #raise NameError("Failed on",myKey)

                #End testing this dict once we reach the limit
                if localTrials==totalTrials:
                    break

        

    def testParadigmDict(self):
        #Simply check that the value of each of the pairs is identical
        #Just manually confirm in PPT

        '''
        #Process for getting underlying cards and lists
        underlyingList = []
        for key in rp.paradigmDict:
            underlyingList.append(rp.paradigmDict[key])
            #if key!=rp.paradigmDict[key]:
                #print(key,rp.paradigmDict[key])
            #    underlyingList.append(rp.paradigmDict[key])
                #print("'"+key+"':0,")
            # rangeCards,rangeMask = rp.evaluate(myKey)
            # rangeCards2,rangeMask2 = rp.evaluate(rp.paradigmDict[key])
        underlyingList = set(underlyingList)
        for key in underlyingList:
            print("'"+key+"':0,")
        '''

        
        #Finally test our macro dict
        for key in dictMacros:
            rangeCards,rangeMask = rp.evaluate(key)
            self.assertTrue(len(rangeCards)==dictMacros[key],msg="Macro range mismatch {} {} {}".format(key,len(rangeCards),dictMacros[key]))


        #First manually test all the underlying values
        for key in paradigmDictUnderlying:
            rangeCards,rangeMask = rp.evaluate(key)
            self.assertTrue(len(rangeCards)==paradigmDictUnderlying[key],msg="Paradigm range mismatch {} {} {}".format(key,len(rangeCards),paradigmDictUnderlying[key]))
        

        #Now we know our underlyingDict values are correct, so we can compare the copies to that dict
        for key in rp.paradigmDict:
            if key!=rp.paradigmDict[key]:
                #If the keys don't match, compare both lookup values in the dictionaries we created
                underlyingVal = paradigmDictUnderlying[rp.paradigmDict[key]]
                copyVal = paradigmDictCopies[key]

                self.assertTrue(underlyingVal==copyVal,msg="Copy range mismatch {} {} {} {}".format(key,rp.paradigmDict[key],underlyingVal,copyVal))

    def testParadigmDictPPT(self):
        '''
        Double check that all the mismatch ranges are the same by comparing their equities in a variety of situations in PPT.
        '''
        for key in rp.paradigmDict:
            if key!=rp.paradigmDict[key]:

                #Compare equity of
                #key
                #rp.paradigmDict[key]

                myQuery = pqlHandVsHand(key,rp.paradigmDict[key],randBoard)
                result = runPQL(myQuery)



    def testParser(self):

        #Want to build random arrays and test the combinations using !:,() etc

        #We will need to use mocks here, as it's calling expand range when it gets down to the base values
        #We want to override it so it just returns the masks we give it.

        #So maybe just give it each possibility?  And we need to build masks somehow

        #So we want to test basic functions.  We need mocks for this.

        #:
        #,
        #!
        #()

        #Creating mock class that overrides function
        class ParserMock(rp.Parser):
            def parseRange(self):
                char = self.peek()
                self.index += 1
                #We just want to return the array
                return char

        #All one or the other
        a1 = np.array([True,True,True,True])
        a2 = np.array([False,False,False,False])

        #3 and 1
        a3 = np.array([False,True,True,True])
        a4 = np.array([True,False,True,True])
        a5 = np.array([True,True,False,True])
        a6 = np.array([True,True,True,False])

        a7 = np.array([True,False,False,True])
        a8 = np.array([False,True,False,True])
        a9 = np.array([False,False,True,True])
        a10 = np.array([False,False,False,True])

        #2 and 2
        a11 = np.array([False,False,True,True])
        a12 = np.array([True,True,False,False])
        a13 = np.array([False,True,False,True])
        a14 = np.array([True,False,True,False])
        a15 = np.array([True,False,False,True])
        a16 = np.array([False,True,True,False])


        p = ParserMock([a11, ',', a12],None)
        handList = p.getValue()
        print(handList)


        exp = [a1, ':', a2]
        exp = [a1, ':', a2, ':', a2]

        exp = [a1, ',', a2]
        exp = [a1, ',', a2, ',', a2]

        exp = [a1, '!', a2]
        exp = [a1, '!', a2, '!', a2]

        exp = [a1, ':', a2, '!', a2]
        exp = [a1, ':', a2, ',', a2]

        exp = [a1, ',', a2, ':', a2]
        exp = [a1, ',', a2, '!', a2]

        exp = [a1, '!', a2, ':', a2]
        exp = [a1, '!', a2, ',', a2]

        [a1, ':', a1, ':', a1, ':', a1]
        [a1, ':', a1, ':', a1, '!', a1]
        [a1, ':', a1, ':', a1, ',', a1]
        [a1, ':', a1, '!', a1, ':', a1]
        [a1, ':', a1, '!', a1, '!', a1]
        [a1, ':', a1, '!', a1, ',', a1]
        [a1, ':', a1, ',', a1, ':', a1]
        [a1, ':', a1, ',', a1, '!', a1]
        [a1, ':', a1, ',', a1, ',', a1]
        [a1, '!', a1, ':', a1, ':', a1]
        [a1, '!', a1, ':', a1, '!', a1]
        [a1, '!', a1, ':', a1, ',', a1]
        [a1, '!', a1, '!', a1, ':', a1]
        [a1, '!', a1, '!', a1, '!', a1]
        [a1, '!', a1, '!', a1, ',', a1]
        [a1, '!', a1, ',', a1, ':', a1]
        [a1, '!', a1, ',', a1, '!', a1]
        [a1, '!', a1, ',', a1, ',', a1]
        [a1, ',', a1, ':', a1, ':', a1]
        [a1, ',', a1, ':', a1, '!', a1]
        [a1, ',', a1, ':', a1, ',', a1]
        [a1, ',', a1, '!', a1, ':', a1]
        [a1, ',', a1, '!', a1, '!', a1]
        [a1, ',', a1, '!', a1, ',', a1]
        [a1, ',', a1, ',', a1, ':', a1]
        [a1, ',', a1, ',', a1, '!', a1]
        [a1, ',', a1, ',', a1, ',', a1]


        [a1, ':', a1, ':', a1, ':', a1, ':', a1]
        [a1, ':', a1, ':', a1, ':', a1, '!', a1]
        [a1, ':', a1, ':', a1, ':', a1, ',', a1]
        [a1, ':', a1, ':', a1, '!', a1, ':', a1]
        [a1, ':', a1, ':', a1, '!', a1, '!', a1]
        [a1, ':', a1, ':', a1, '!', a1, ',', a1]
        [a1, ':', a1, ':', a1, ',', a1, ':', a1]
        [a1, ':', a1, ':', a1, ',', a1, '!', a1]
        [a1, ':', a1, ':', a1, ',', a1, ',', a1]
        [a1, ':', a1, '!', a1, ':', a1, ':', a1]
        [a1, ':', a1, '!', a1, ':', a1, '!', a1]
        [a1, ':', a1, '!', a1, ':', a1, ',', a1]
        [a1, ':', a1, '!', a1, '!', a1, ':', a1]
        [a1, ':', a1, '!', a1, '!', a1, '!', a1]
        [a1, ':', a1, '!', a1, '!', a1, ',', a1]
        [a1, ':', a1, '!', a1, ',', a1, ':', a1]
        [a1, ':', a1, '!', a1, ',', a1, '!', a1]
        [a1, ':', a1, '!', a1, ',', a1, ',', a1]
        [a1, ':', a1, ',', a1, ':', a1, ':', a1]
        [a1, ':', a1, ',', a1, ':', a1, '!', a1]
        [a1, ':', a1, ',', a1, ':', a1, ',', a1]
        [a1, ':', a1, ',', a1, '!', a1, ':', a1]
        [a1, ':', a1, ',', a1, '!', a1, '!', a1]
        [a1, ':', a1, ',', a1, '!', a1, ',', a1]
        [a1, ':', a1, ',', a1, ',', a1, ':', a1]
        [a1, ':', a1, ',', a1, ',', a1, '!', a1]
        [a1, ':', a1, ',', a1, ',', a1, ',', a1]
        [a1, '!', a1, ':', a1, ':', a1, ':', a1]
        [a1, '!', a1, ':', a1, ':', a1, '!', a1]
        [a1, '!', a1, ':', a1, ':', a1, ',', a1]
        [a1, '!', a1, ':', a1, '!', a1, ':', a1]
        [a1, '!', a1, ':', a1, '!', a1, '!', a1]
        [a1, '!', a1, ':', a1, '!', a1, ',', a1]
        [a1, '!', a1, ':', a1, ',', a1, ':', a1]
        [a1, '!', a1, ':', a1, ',', a1, '!', a1]
        [a1, '!', a1, ':', a1, ',', a1, ',', a1]
        [a1, '!', a1, '!', a1, ':', a1, ':', a1]
        [a1, '!', a1, '!', a1, ':', a1, '!', a1]
        [a1, '!', a1, '!', a1, ':', a1, ',', a1]
        [a1, '!', a1, '!', a1, '!', a1, ':', a1]
        [a1, '!', a1, '!', a1, '!', a1, '!', a1]
        [a1, '!', a1, '!', a1, '!', a1, ',', a1]
        [a1, '!', a1, '!', a1, ',', a1, ':', a1]
        [a1, '!', a1, '!', a1, ',', a1, '!', a1]
        [a1, '!', a1, '!', a1, ',', a1, ',', a1]
        [a1, '!', a1, ',', a1, ':', a1, ':', a1]
        [a1, '!', a1, ',', a1, ':', a1, '!', a1]
        [a1, '!', a1, ',', a1, ':', a1, ',', a1]
        [a1, '!', a1, ',', a1, '!', a1, ':', a1]
        [a1, '!', a1, ',', a1, '!', a1, '!', a1]
        [a1, '!', a1, ',', a1, '!', a1, ',', a1]
        [a1, '!', a1, ',', a1, ',', a1, ':', a1]
        [a1, '!', a1, ',', a1, ',', a1, '!', a1]
        [a1, '!', a1, ',', a1, ',', a1, ',', a1]
        [a1, ',', a1, ':', a1, ':', a1, ':', a1]
        [a1, ',', a1, ':', a1, ':', a1, '!', a1]
        [a1, ',', a1, ':', a1, ':', a1, ',', a1]
        [a1, ',', a1, ':', a1, '!', a1, ':', a1]
        [a1, ',', a1, ':', a1, '!', a1, '!', a1]
        [a1, ',', a1, ':', a1, '!', a1, ',', a1]
        [a1, ',', a1, ':', a1, ',', a1, ':', a1]
        [a1, ',', a1, ':', a1, ',', a1, '!', a1]
        [a1, ',', a1, ':', a1, ',', a1, ',', a1]
        [a1, ',', a1, '!', a1, ':', a1, ':', a1]
        [a1, ',', a1, '!', a1, ':', a1, '!', a1]
        [a1, ',', a1, '!', a1, ':', a1, ',', a1]
        [a1, ',', a1, '!', a1, '!', a1, ':', a1]
        [a1, ',', a1, '!', a1, '!', a1, '!', a1]
        [a1, ',', a1, '!', a1, '!', a1, ',', a1]
        [a1, ',', a1, '!', a1, ',', a1, ':', a1]
        [a1, ',', a1, '!', a1, ',', a1, '!', a1]
        [a1, ',', a1, '!', a1, ',', a1, ',', a1]
        [a1, ',', a1, ',', a1, ':', a1, ':', a1]
        [a1, ',', a1, ',', a1, ':', a1, '!', a1]
        [a1, ',', a1, ',', a1, ':', a1, ',', a1]
        [a1, ',', a1, ',', a1, '!', a1, ':', a1]
        [a1, ',', a1, ',', a1, '!', a1, '!', a1]
        [a1, ',', a1, ',', a1, '!', a1, ',', a1]
        [a1, ',', a1, ',', a1, ',', a1, ':', a1]
        [a1, ',', a1, ',', a1, ',', a1, '!', a1]
        [a1, ',', a1, ',', a1, ',', a1, ',', a1]


        #This is fine, we'd also like to test parenthesis
        ['(', a1, ',', a1, ')', '!', a1]

        [a1, ',', '(', a1, ':', a1, ')']
        
        ['(', a1, ',', a1, ',', a1, ')', ':', a1]

        [a1, '!', '(', a1, ',', a1, ',', a1, ')', ':', a1]

        [a1, '!', '(', a1, ':', a1, '!', a1, ')']
        
        [a1, '!', '(', a1, ':', a1, ')', '!', a1]

        ['(', a1, '!', a1, ',', a1, ')', '!', a1, ',', '(', a1, ':', a1, ')', '!', a1]
        [a1, ':', '(', a1, '!', a1, ',', a1, ')', '!', a1, ',', '(', a1, ':', a1, ')', '!', a1]
        
        ['(', '(', a1, ':', a1, ')', '!', a1, ')', ',', a1]

        ['(', '(', a1, ':', a1, ')', ',', a1, ')', ',' , a1]

        ['(', '(', a1, ':', a1, ')', '!', '(', a1, '!', a1, ')', ')', '!' , a1]
        


        p = ParserMock([a11, ',', a12],None)

        #handList here will be a mask
        handList = p.getValue()

        print(handList)





v1SyntaxValidRivExpressions = ['A','s','As','A-5','As-5s','Ts-','Ts+','8+','9-','A,Ks,Qs','Js-4s,As']

v1SyntaxInvalidRivExpressions = ['AA','ss','Aq','A-5c','As-5h','Ts-+','Ts+-','Ts++','Ts--','8+9','09-','09+','09','A,Ks;Qs','[A]','s+','As,,Ks',',A-5','As-5s,']



v2SyntaxValidatorInvalidList=['AsKhJd2q','AAAAA','AA0,KK','AxxAyxy','AA$dss','AA$$ss','KJ*5+s','*****','15%%','1015%','30%-50%+','PRON','TT-76','TT-7',
             'TT-7-','TT-77+','TT+77','TTc-77','TTc-77d','[TT-76]','[TT-7]','[TT-7-]','[TT-77+]','[TT+77]','[TTc-77]','[TTc-77d]','Q+Q',
             '98765-','[A-J][2-5]333','[2s,Jc,TJ]','AARRR','155%','155%6h','30%+50%6h','T8-52','T8c-52c','[KQcJ-7s6c5]','76c++','QJTc--',
             '[A-J][55+]RO','[KK-][T+][5c-][Jh]','+','-','-5','[+]','[-]','[-Jc]','()','(K(J))','[(Kc)]','[(Kc])','Kc,,Jc','Kc!:Jc','Kc+-Jc',
             'Kc-Jc+','Kc-Jc+','Kc-(Jc+)','Kc-,(Jc+)+',')Kc-,(Jc+)(',',Kc-,Jc','!Kc-,Jc',':Kc-,Jc','],Kc-,Jc','Kc-,Jc[]','Kc-,Jc,[]','Kc.','Kc:','Kc!']



v2SyntaxValidatorValidList=['A','AsKhJd2c','AA','AA,KK','AxAyxy','AA$ds','AxAyxz','AA$ss','KJ*ss','*','15%','10%','30%-50%','K','ss','JRON','RROO','hhxx',
           'TT-77','Q+','9876-','A-Q','[A-J][2-5]33','K[2s,Jc,T]','J[T-][T-][T-]','*$np','*$nt','AA!AAA','AA$nt','AARR','A!K','25%:wxyz',
           'A:15%!AA','40%!RR','([T+][T+][T+],ss):15%','**KJs','30%-50%6h','T8-53','T8c-53c','[KQcJ-76c5]','76c+','QJTc-','[A-J][5+]RO',
           '[K-][T+][5c-][Jh]','****','(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:16%6h,xxyz:12%6h),Axxy!RR:(xxyy:18%6h),*!RR![6-]:(xxyy:12%6h,xxyy!A),OORR:xxy,$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy:30%6h,xxyz:12%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy:18%6h,xxyz:10%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:16%6h),(KQ9-,KJ9-)!RR:(xxyy:12%6h),(4556+,4456+,6654+):(xxyy:18%6h,xxyz:12%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:14%6h,xxyz:12%6h))$nt',
           '(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64,KT-74):xxy, KK:(3%6h,xxyy,AQ,QJ-65,QT-64):xxy, QQ:xxyy, JJ:(xxyy:6%6h,xxyy!A:8%6h), AK!RR:xxyy, Axxy!RR:(xxyy:12%6h,xxyz:10%6h), *!RR![6-]:xxyy, OORR:(xxyy,xxyz:45%6h), $0G:60%6h, $1G:(xxyy:55%6h,xxyz:55%6h,xxy:45%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:24%,xxyz:16%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:18%6h,xxyz:12%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:18%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:12%6h,Axxyy:20%6h), (4556+,4456+,6654+):(xxyy:16%6h,xxyz:14%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:14%6h,xxyz:12%6h))$nt',
           '(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy,xxyz:16%6h),Axxy!RR:(xxyy:26%6h),*!RR![6-]:(xxyy,xxy:10%6h),OORR:xxy,$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy,xxy:20%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy:24%6h,xxy:12%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:20%6h),(KQ9-,KJ9-)!RR:(xxyy:16%6h),(4556+,4456+,6654+):(xxyy,xxyz:20%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy,xxyz:18%6h))$nt',
           '(*!RRR:2%6h, AA:xxy, KK:(4%6h,xxyy,AQ,QJ-65,QT-64):xxy, QQ:xxyy, JJ:(xxyy:6%6h,xxyy!A:8%6h), AK!RR:(xxyy,xxyz:12%6h), Axxy!RR:(xxyy:15%6h,xxyz:12%6h), *!RR![6-]:(xxyy,xxyz:12%6h), OORR:(xxyy,xxyz:50%6h), $0G:60%6h, $1G:(xxyy:55%6h,xxyz:55%6h,xxy:45%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:40%6h,xxyz:20%6h,xxy:15%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:30%6h,xxyz:20%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:24%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:18%6h,Axxyy:20%6h), (4556+,4456+,6654+):(xxyy:22%6h,xxyz:18%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:18%6h,xxyz:16%6h))$nt',
           '(*!RRR:3%6h,AA:xxy,KK:4%6h,QQ:(xxyy:2%6h,xxyy!A:6%6h),JJ:(xxyy:4%6h,xxyy!A:8%6h),AK!RR:(xxyy,xxyz:16%6h),Axxy!RR:(xxyy,xxyz:16%6h),*!RR![6-]:(xxyy,xxyz:14%6h),OORR,$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy,xxy:24%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy,xxy:16%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:34%6h),(KQ9-,KJ9-)!RR:(xxyy:32%6h),(4556+,4456+,6654+):(xxyy,xxyz:28%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy,xxyz:22%6h))$nt',
           '(*!RRR:2%6h, AA:(xxy,JT+), KK:(xxy,AQ), QQ:xxyy, JJ:xxyy, AK!RR:(xxyy,xxy:14%6h), Axxy!RR:(xxyy:15%6h,xxy:15%6h), *!RR![6-]:(xxyy,xxy:18%6h), OORR, $0G:60%6h, $1G:(xxyy:55%6h,xxyz:55%6h,xxy:45%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:40%6h,xxyz:30%6h,xxy:25%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:30%6h,xxyz:25%6h,xxy:15%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:20%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:20%6h,Axxyy:20%6h), (4556+,4456+,6654+):(xxyy:30%6h,xxyz:24%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:24%6h,xxyz:20%6h))$nt',
           '(*!RRR:1%6h,AA:(xxyy,56+,46+):xxy,KK:2%6h,QQ:2%6h,JJ:3%6h,AK!RR:3%6h,Axxy!RR:3%6h,*!RR![6-]:3%6h,OORR:(8%6h!JJ+),$0G:(xxyy:30%6h),$1G:(xxyy:26%6h))$nt',
           '(*!RRR:1%6h,AA:(xxyy,56+,46+):xxy,KK:2%6h,QQ:2%6h,JJ:3%6h,AK!RR:3%6h,Axxy!RR:3%6h,*!RR![6-]:3%6h,OORR:(8%6h!JJ+),$0G:(xxyy:30%6h),$1G:(xxyy:26%6h))$nt',
           '(*!RRR:2%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:4%6h),Axxy!RR:(xxyy:4%6h),*!RR![6-]:(xxyy:4%6h,xxyy!A),OORR:(xxyy:20%6h!JJ+),$0G:(xxyy:42%6h),$1G:(xxyy:30%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:8%6h),(KQ9-,KJ9-)!RR:(xxyy:6%6h),(4556+,4456+,6654+):(xxyy:10%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:10%6h))$nt',
           '(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64):xxy, KK:2%6h, QQ:(xxyy:2%6h,xxyy!A:4%6h), JJ:(xxyy:4%6h,xxyy!A:6%6h), AK!RR:(xxyy:4%6h), Axxy!RR:(xxyy:4%6h), *!RR![6-]:(xxyy:6%6h,xxyy!A), OORR:(xxyy:20%6h!JJ+), $0G:(xxyy:50%6h, xxyz:45%6h), $1G:(xxyy:30%6h, xxyz:20%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:10%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:8%6h), (KQ9-,KJ9-)!RR:(xxyy:6%6h), (4556+,4456+,6654+):(xxyy:8%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:6%6h))$nt',
           '(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:6%6h),Axxy!RR:(xxyy:6%6h),*!RR![6-]:(xxyy:6%6h,xxyy!A),OORR:((xxyy:40%6h,xxyz:20%6h)!JJ+),$0G:(xxyy,xxyz:60%6h),$1G:(xxyy:30%6h,xxyz:50%6h),(AQT9-, AKJ9-, AQJ9-):(xxyy:20%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:10%6h),(KQ9-,KJ9-)!RR:(xxyy:8%6h),(4556+,4456+,6654+):(xxyy:15%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:10%6h))$nt',
           '(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64,KT-74):xxy, KK:(2%6h,xxyy), QQ:(xxyy:2%6h,xxyy!A:4%6h), JJ:(xxyy:4%6h,xxyy!A:6%6h), AK!RR:(xxyy:6%6h), Axxy!RR:(xxyy:6%6h), *!RR![6-]:(xxyy,xxyy!A), OORR:((xxyy,xxyz:25%6h)!JJ+), $0G:(xxyy:50%6h, xxyz:50%6h), $1G:(xxyy:30%6h,xxyz:50%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:16%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:8%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:12%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:8%6h,Axxyy:16%6h), (4556+,4456+,6654+):(xxyy:12%6h,xxyz:10%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:10%6h,xxyz:8%6h))$nt',
           '(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:12%6h),Axxy!RR:(xxyy:10%6h),*!RR![6-]:(xxyy:8%6h,xxyy!A),OORR:((xxyy,xxyz:30%6h)!JJ+),$0G:50%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy:24%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy:16%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:15%6h),(KQ9-,KJ9-)!RR:(xxyy:12%6h),(4556+,4456+,6654+):(xxyy:18%6h,xxyz:10%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:12%6h,xxyz:10%6h))$nt',
           '(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64,KT-74):xxy, KK:(2%6h,xxyy,AQ,QJ-98):xxy, QQ:xxyy, JJ:(xxyy:6%6h,xxyy!A:8%6h), AK!RR:(xxyy:8%6h), Axxy!RR:(xxyy:10%6h), *!RR![6-]:xxyy, OORR:((xxyy,xxyz:50%6h)!QQ+), $0G:60%6h, $1G:(xxyy:42%6h,xxyz:50%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:20%,xxyz:10%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:16%6h,xxyz:10%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:16%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:8%6h,Axxyy:16%6h), (4556+,4456+,6654+):(xxyy:14%6h,xxyz:12%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:12%6h,xxyz:10%6h))$nt',
           '(AA:2%6h,AK!RR:3%6h,(OORR)!(JJ+):4%6h,$0G:10%6h)$nt',
           '(AA:3%6h, AKK:3%6h, AK!RR:3%6h, (OORR)!(JJ+):4%6h, $0G:12%6h, $1G:7%6h)$nt',
           '(AA, AKK:4%, KK:3%, AQQ:2%, AK!RR:5%, (OORR)!(JJ+):5%, $0G:17%, $0G![J+]:24%, $1G:8%, $1G![J+]:12%, (AQT9-, AKJ9-, AQJ9-):4%, (AKJ8-, AQ98-, AQJ8-):4%)$nt',
           '(AA, AKK:5%, KK:4%, AQQ:3%, AK!RR:6%, (OORR)!(JJ+):6%, $0G:21%, $0G![J+]:30%, $1G:11%, $1G![J+]:16%, (AQT9-, AKJ9-, AQJ9-):6%, (AKJ8-, AQ98-, AQJ8-):6%)$nt',
           '(AA, AKK:6%, KK:5%, AQQ:3%, AK!RR:7%, (OORR)!(JJ+):8%, $0G:30%, $0G![J+]:42%, $1G:16%, $1G![J+]:20%, (AQT9-, AKJ9-, AQJ9-):8%, (AKJ8-, AQ98-, AQJ8-):8%)$nt',
           '(*!RRR:8%6h,AA:8%6h,KK:6%6h,QQ:7%6h,JJ:6%6h,AK!RR:7%6h,Axxy!RR:13%6h,*!RR![6-]:8%6h,OORR:(20%6h!JJ+),$0G:50%6h,$1G:28%6h,(AQT9-, AKJ9-, AQJ9-):21%6h,(AKJ8-, AQ98-, AQJ8-):10%6h,(KQJ-,KQT-,KJT-)!RR:10%6h,(KQ9-,KJ9-)!RR:8%6h,(4556+,4456+,6654+):25%6h,(3556+,4457+,4476+,4463+,6643+,6653+):16%6h)$nt',
           '(*!RRR:10%6h,AA:10%6h,KK:9%6h,QQ:10%6h,JJ:9%6h,AK!RR:10%6h,Axxy!RR:16%6h,*!RR![6-]:13%6h,OORR:(25%6h!JJ+),$0G:60%6h,$1G:34%6h,(AQT9-, AKJ9-, AQJ9-):25%6h,(AKJ8-, AQ98-, AQJ8-):14%6h,(KQJ-,KQT-,KJT-)!RR:14%6h,(KQ9-,KJ9-)!RR:10%6h,(4556+,4456+,6654+):30%6h,(3556+,4457+,4476+,4463+,6643+,6653+):20%6h)$nt',
           '(*!RRR:14%6h,AA:16%6h,KK:14%6h,QQ:15%6h,JJ:14%6h,AK!RR:14%6h,Axxy!RR:23%6h,*!RR![6-]:20%6h,OORR:(35%6h!JJ+),$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):34%6h,(AKJ8-, AQ98-, AQJ8-):21%6h,(KQJ-,KQT-,KJT-)!RR:20%6h,(KQ9-,KJ9-)!RR:16%6h,(4556+,4456+,6654+):40%6h,(3556+,4457+,4476+,4463+,6643+,6653+):23%6h)$nt',
           '(*!RRR:18%6h,AA:20%6h,KK:18%6h,QQ:19%6h,JJ:19%6h,AK!RR:19%6h,Axxy!RR:30%6h,*!RR![6-]:25%6h,OORR:(45%6h!JJ+),$0G:70%6h,$1G:50%6h,(AQT9-, AKJ9-, AQJ9-):42%6h,(AKJ8-, AQ98-, AQJ8-):25%6h,(KQJ-,KQT-,KJT-)!RR:24%6h,(KQ9-,KJ9-)!RR:20%6h,(4556+,4456+,6654+):50%6h,(3556+,4457+,4476+,4463+,6643+,6653+):28%6h)$nt',
           '(*!RRR:22%6h,AA:24%6h,KK:22%6h,QQ:24%6h,JJ:24%6h,AK!RR:25%6h,Axxy!RR:37%6h,*!RR![6-]:30%6h,OORR:(55%6h!QQ+),$0G:80%6h,$1G:60%6h,(AQT9-, AKJ9-, AQJ9-):49%6h,(AKJ8-, AQ98-, AQJ8-):30%6h,(KQJ-,KQT-,KJT-)!RR:30%6h,(KQ9-,KJ9-)!RR:24%6h,(4556+,4456+,6654+):60%6h,(3556+,4457+,4476+,4463+,6643+,6653+):36%6h)!kkk',
           '(*!RRR:32%6h,AA:40%6h,KK:36%6h,QQ:36%6h,JJ:36%6h,AK!RR:36%6h,Axxy!RR:56%6h,*!RR![6-]:40%6h,OORR:75%6h,$0G:90%6h,$1G:80%6h,(AQT9-, AKJ9-, AQJ9-):64%6h,(AKJ8-, AQ98-, AQJ8-):40%6h,(KQJ-,KQT-,KJT-)!RR:40%6h,(KQ9-,KJ9-)!RR:32%6h,(4556+,4456+,6654+):80%6h,(3556+,4457+,4476+,4463+,6643+,6653+):47%6h)!kkk-',
           '(*!RRR:40%6h,AA,KK,QQ:50%6h,JJ:50%6h,AK!RR:50%6h,Axxy!RR:66%6h,*!RR![6-]:50%6h,OORR,$0G,$1G,(AQT9-, AKJ9-, AQJ9-):74%6h,(AKJ8-, AQ98-, AQJ8-):64%6h,(KQJ-,KQT-,KJT-)!RR:60%6h,(KQ9-,KJ9-)!RR:50%6h,(4556+,4456+,6654+),(3556+,4457+,4476+,4463+,6643+,6653+):52%6h)!kkk-']


fixitList = ['(Ax[2x-5x], 2x3x-2x5x, 3x4x-3x5x, 4x5x):30%-50%']


import subprocess

def runPQL(query):
    r = subprocess.check_output(['java', "-cp", "p2.jar", "propokertools.cli.RunPQL", query], cwd='C:\\Program Files\\PPTOddsOracle\\ui_jar',shell=True)
    return(r.decode("utf-8"))


def pqlHandVsHand(h1, h2, board):
    if len(board)>0:
        useBoard = "board='"+board+"',"
    else:
        useBoard = ""

    pqlQuery = ("select /* Start equity stats */"
                "avg(riverEquity(PLAYER_1)) as PLAYER_1_equity1,"
                "count(winsHi(PLAYER_1)) as PLAYER_1_winsHi1,"
                "count(tiesHi(PLAYER_1)) as PLAYER_1_tiesHi1,"
                "avg(riverEquity(PLAYER_2)) as PLAYER_2_equity1,"
                "count(winsHi(PLAYER_2)) as PLAYER_2_winsHi1,"
                "count(tiesHi(PLAYER_2)) as PLAYER_2_tiesHi1"
                "/* End equity stats */ "
                "from game='omahahi', syntax='Generic',"
                "{}"
                "PLAYER_1='{}',"
                "PLAYER_2='{}'").format(useBoard,h1,h2)
    
    return pqlQuery


#mquery = pqlHandVsHand('AcKcQcJc','Tc9c8c7c','AdQd5d3d2d')
#f = runPQL(mquery)
#print(f)

#hRange = '$fi40!$3b12o'
#vals,valMask = rp.evaluate(hRange,board=None,rangeFilter=None)
#print(len(vals))
runTests = testRangeParserMasks()
#runTests.testParadigmDict()

#runTests.testParser()
#runTests.testParadigmDict()

runTests.testRanges()

'''
So run test comparing our dictionary lookup values to what we have
And then run another test comparing EVs of the two ranges in a variety of situations

'''

