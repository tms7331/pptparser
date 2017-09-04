import itertools
import re
import numpy as np
import os

import SyntaxValidator as sv

ploDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ploDir = ploDir + '/PPTParser/'
retFile = np.load(ploDir+'npfiles/pptRankedHUnums.npy')


ALLRANKS = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
ALLRANKVARS = ['R','O','N','P']

ALLSUITS = ['C','S','D','H']
ALLSUITVARS = ['W','X','Y','Z']



patternDict = {
'NO':'NO','WN':'WN','WX':'WX','NN':'NN','WW':'WW','WXY':'WXY','NNW':'NN','NWO':'NO','WNW':'WW','WNX':'WX','NNN':'NNN','NNO':'NNO','WNN':'NN',
'NOW':'NO','NOO':'NNO','NOP':'NOP','WNO':'NO','WWN':'WW','WXN':'WX','WWW':'WWW','WWX':'WWX','WXX':'WWX','WWNO':'WWNO','WXNN':'WXNN','NWNX':'NN',
'WWNW':'WWW','WXNW':'WWX','WWNX':'WWX','WXNY':'WXY','WXNX':'WWX','WWWN':'WWW','WWXN':'WWX','WXXN':'WWX','WXYN':'WXY','WNNX':'NN','NWOW':'WW',
'WNOW':'WW','WNWO':'WW','NOWP':'NOP','NOPW':'NOP','WNOP':'NOP','NWOP':'NOP','NNWO':'NNO','NWOO':'NNO','NOOW':'NNO','WNNO':'NNO','WNOO':'NNO',
'NNOW':'NNO','NNNW':'NNN','WNNN':'NNN','NNOP':'NNOP','NOOP':'NNOP','NNOO':'NNOO','WXYZ':'WXYZ','WWXX':'WWXX','WWXY':'WWXY','WXYY':'WWXY',
'WXXY':'WWXY','WWWX':'WWWX','WXXX':'WWWX','WWWW':'WWWW','NOPR':'NOPR','NOPP':'NNOP','NNNO':'NNNO','NOOO':'NNNO','NNNN':'NNNN','NWOX':'NWOX',
'WNXO':'NWOX','WXNO':'NWOX','WNOX':'NWOX','WWNN':'NNOWW','WNNW':'NWNOW','WXNNY':'WXNNY','NWOOX':'NNO','NWNOX':'NNO','NWNXO':'NNO','WNNXO':'NNO',
'WNOOX':'NNO','NNWOX':'NNO','NOWOX':'NNO','WNNNX':'NNN','NWNXN':'NNN','NNWNX':'NNN','WNXOX':'WWX','WXNWO':'WWX','WXNXO':'WWX','WNWOX':'WWX',
'WXNOW':'WWX','WNXOW':'WWX','WXNOX':'WWX','WNWOW':'WWW','WWNWO':'WWW','WWNOW':'WWW','NWOPR':'NOPR','NOPRW':'NOPR','NOWPR':'NOPR','NOPWR':'NOPR',
'NNWOP':'NNOP','NWOOP':'NNOP','NOWPP':'NNOP','NOOPW':'NNOP','NOPPW':'NNOP','NNOWP':'NNOP','NOOWP':'NNOP','NWOPP':'NNOP','NNOPW':'NNOP',
'NNWOO':'NNOO','NNOOW':'NNOO','NOOOW':'NNNO','NNNOW':'NNNO','NNNWO':'NNNO','NWOOO':'NNNO','NNNNW':'NNNN','WXYNZ':'WXYZ','WXXNW':'WWXX',
'WXYNW':'WWXY','WWXNY':'WWXY','WXYNY':'WWXY','WXYNX':'WWXY','WXXNY':'WWXY','WWWNX':'WWWX','WWXNW':'WWWX','WXXNX':'WWWX','WWWNW':'WWWW',
'WWXNX':'WWXX','WNXNY':'NWNXY','WWNXO':'WWNXO','WWNOX':'WWNXO','NWNOW':'NWNOW','NWOWP':'NWOWP','NOWPW':'NWOWP','NWOPW':'NWOWP','WNXOO':'NNOWX',
'WNNOX':'NNOWX','WNWOP':'WNWOP','WNOWP':'WNWOP','WNOPW':'WNWOP','WXNOY':'NWOXY','WXNYO':'NWOXY','WNXOY':'NWOXY','WNWOO':'NNOWW','WWNNX':'NNOWW',
'WNNOW':'NNOWW','WXNNW':'NWNOWX','WXNNX':'NWNOWX','NWOXP':'NWOXP','WNOPX':'NWOXP','WNXOP':'NWOXP','NWOPX':'NWOXP','NOWPX':'NWOXP',
'WNOXP':'NWOXP','WNOOW':'WNOOW','WNNWO':'WNOOW','WNWNX':'NWNOW','NWOOW':'NWNOW','NNWOW':'NWNOW','WNXNW':'NWNOW','WNNNW':'NWNNOW',
'WWNNW':'NWNOWPW','NWOXPY':'NWOXPY','WNNXNY':'NNN','NWNXNY':'NNN','NWOWPW':'WWW','WNWOWP':'WWW','WNOWPW':'WWW','WNWOPW':'WWW','NOOWPX':'NNOP',
'NOPWPX':'NNOP','NNWOPX':'NNOP','NNWOXP':'NNOP','NWNXOP':'NNOP','NWOOXP':'NNOP','NWOPPX':'NNOP','NOWOXP':'NNOP','NOWPPX':'NNOP','NWNXOO':'NNOO',
'NNWOOX':'NNOO','NNOWOX':'NNOO','NOOWOX':'NNNO','NWOOOX':'NNNO','NNNWOX':'NNNO','NWNXNO':'NNNO','NNWNXO':'NNNO','NWNNOX':'NNNO','WXNYOX':'WWXY',
'WXNYOY':'WWXY','NNNWNX':'NNNN','WWNXOX':'WWXX','WXNWOX':'WWXX','NWOXWX':'WWXX','WXNXOW':'WWXX','WXNXOY':'WWXY','WXNYOW':'WWXY','WXNWOY':'WWXY',
'WXNWOW':'WWWX','WWNWOW':'WWWW','WWNWOX':'WWWX','WWNXOW':'WWWX','WXNXOX':'WWWX','NWNXOY':'NWNXOY','WNOXOY':'NWNXOY','NWOXOY':'NWNXOY',
'WNXNYO':'NWNXOY','WNXOYP':'WNXOYP','WNXOPY':'WNXOYP','WNOXPY':'WNXOYP','WXNYNZ':'NWNXYZ','WWNXOY':'NWOXYY','WXNYOZ':'NWOXYZ','WNNWOX':'WNNWOX',
'WNXOOW':'WNNWOX','NWOXPP':'NWOXPP','NNOWPX':'NWOXPP','NWOOPX':'NWOXPP','WNXOOY':'NWNOXY','WNNXOY':'NWNOXY','NWOWPP':'NWOWPP','WNXOOX':'NWNOWX',
'WNNXOX':'NWNOWX','WNOXOW':'WNOOW','WNXNWO':'WNOOW','WNWNXO':'WNOOW','WNOWOX':'WNOOW','WNXOWP':'WNXOWP','WNXOPW':'WNXOWP','WNOWPX':'WNXOWP',
'WNWOXP':'WNXOWP','WNWOPX':'WNXOWP','WNOXPW':'WNXOWP','NWOWPR':'NWOWPR','NWOPRW':'NWOWPR','NOPWRW':'NWOWPR','NOWPRW':'NWOWPR','NOWPWR':'NWOWPR',
'NWOPWR':'NWOWPR','WWNXNY':'NWNXYY','NNWOOW':'NWNXOWO','NWOXPR':'NWOXPR','NOWPRX':'NWOXPR','NWOPXR':'NWOXPR','NOPWRX':'NWOXPR','NOWPXR':'NWOXPR',
'NWOPRX':'NWOXPR','NWOWPX':'NWOWPX','NWOXPX':'NWOWPX','WNXOPX':'NWOWPX','NWOXPW':'NWOWPX','WNOXPX':'NWOWPX','WNXOXP':'NWOWPX','NWOOPW':'NWOWPP',
'NNOWPW':'NWOWPP','WXNWNX':'NWNXWX','WNWOOX':'NNOWW','WNNXOW':'NNOWW','NWNXOX':'NWNOW','NWOXOW':'NWNOW','NWNXOW':'NWNOW','NWOWOX':'NWNOW',
'NWNNOW':'NWNNOW','WNNWNX':'NWNNOW','NNNWOW':'NWNNOW','NWOOOW':'NWNNOW','WNNXNW':'NWNNOW','NNWOWP':'NWNXOXP','NWOPPW':'NWNXOXP','NOWPPW':'NWNXOXP',
'NNWOPW':'NWNXOXP','NOOWPW':'NWNXOXP','NWOOWP':'NWNXOXP','NWNOWP':'NWNXOXP','WWNWNX':'NWNOWPW','WNNWOW':'NWNOWPW','WNWOOW':'NWNOWPW',
'WWNXNW':'NWNOWPW','WXNYNX':'NWNXOWY','WXNWNY':'NWNXOWY','WXNYNW':'NWNXOWY','WXNXNY':'NWNXOWY','WNWOWPW':'WWWW','NNWNXOY':'NNNO','NWNXNYO':'NNNO',
'NOWOXOY':'NNNO','NWOOXOY':'NNNO','NNWNXNY':'NNNN','WNWOXPW':'WWWX','WNXOXPX':'WWWX','WNWOWPX':'WWWX','WNXOWPW':'WWWX','WNXNYNZ':'NWNXNYZ',
'NWNXOYO':'NWNXOYO','NNWOXOY':'NWNXOYO','NWNXOOY':'NWNXOYO','WNXNYOZ':'NWNXOYZ','WNXOYOZ':'NWNXOYZ','WNXOWPY':'NWOXPYW','WNWOXPY':'NWOXPYW',
'WNXOYPW':'NWOXPYW','NWNOXPY':'NWNOXPY','NNWOXPY':'NWNOXPY','NWOOXPY':'NWNOXPY','NWOXPPY':'NWNOXPY','NWOWPWR':'NWOWPWR','NWOWPRW':'NWOWPWR',
'NWOPWRW':'NWOWPWR','NOWPWRW':'NWOWPWR','WNWOXPX':'NWOWPXX','WNXOWPX':'NWOWPXX','WNXOXPW':'NWOWPXX','NWNXNOY':'NNNO','WNXOXPY':'NWOWPXY',
'WNXOYPX':'NWOWPXY','WNXOYPY':'NWOWPXY','NWOXPYR':'NWOXPYR','NOWPXRY':'NWOXPYR','NWOXPRY':'NWOXPYR','NWOPXRY':'NWOXPYR','WNWOXOY':'NWNXYY',
'WNXNYOW':'NWNXYY','NWNXOWO':'NWNXOWO','NWNXOOW':'NWNXOWO','NWNXOOX':'NWNXOWO','NNWOWOX':'NWNXOWO','NNWOXOW':'NWNXOWO','WNWNXOY':'NWNXOYW',
'WNXNWOY':'NWNXOYW','WNXOWOY':'NWNXOYW','WNXOYOW':'NWNXOYW','NWNXOYP':'NWNXOYP','NOWOXPY':'NWNXOYP','NWOPXPY':'NWNXOYP','NOWPXPY':'NWNXOYP',
'NWOXOYP':'NWNXOYP','NWNXOPY':'NWNXOYP','NWOOXPW':'NWOWPP','NNWOXPX':'NWOWPP','NWOWPPX':'NWOWPP','NWNOXPX':'NWOWPP','NWNOWPX':'NWNOWPX',
'NNWOXPW':'NWNOWPX','NWOXPPW':'NWNOWPX','NWOOWPX':'NWNOWPX','NWOOXPX':'NWNOWPX','NWOXPPX':'NWNOWPX','NNWOWPX':'NWNOWPX','WNWNXOX':'NWNXWX',
'WNXNWOX':'NWNXWX','WNXOXOW':'NWNXWX','WNXOWOX':'NWNXWX','NNWNXOW':'NWNNOW','WNXNYNW':'NWNNOW','NNWNXOX':'NWNNOW','NWNXNOW':'NWNNOW',
'WNXNWNY':'NWNNOW','NWOOXOW':'NWNNOW','WNWNXNY':'NWNNOW','NWOOWOX':'NWNNOW','NWNXOXP':'NWNXOXP','NWOXOWP':'NWNXOXP','NOWPXPW':'NWNXOXP',
'NWNXOPW':'NWNXOXP','NWOWOXP':'NWNXOXP','NWOPWPX':'NWNXOXP','NOWOXPW':'NWNXOXP','NOWPWPX':'NWNXOXP','NWOPXPW':'NWNXOXP','NOWOXPX':'NWNXOXP',
'NWNXOWP':'NWNXOXP','NWNXOPX':'NWNXOXP','NWNOWPW':'NWNOWPW','WNXNWOW':'NWNOWPW','WNWOWOX':'NWNOWPW','NWOOWPW':'NWNOWPW','WNWOXOW':'NWNOWPW',
'NWOWPPW':'NWNOWPW','WNWNXOW':'NWNOWPW','NNWOWPW':'NWNOWPW','NWOWPXR':'NWOWPXR','NOWPWRX':'NWOWPXR','NWOXPRX':'NWOWPXR','NWOPWRX':'NWOWPXR',
'NWOXPWR':'NWOWPXR','NWOXPXR':'NWOWPXR','NOWPXRW':'NWOWPXR','NOWPXRX':'NWOWPXR','NWOWPRX':'NWOWPXR','NWOPXRW':'NWOWPXR','NWOXPRW':'NWOWPXR',
'NWOPXRX':'NWOWPXR','WNXNYOX':'NWNXOWY','WNXNYOY':'NWNXOWY','WNXOXOY':'NWNXOWY','WNXOYOX':'NWNXOWY','WNXOYPZ':'NWOXPYZ','NWNXOWOX':'NWNXOWOX',
'NWNXOYOZ':'NWNXOYOZ','NWOXPYRZ':'NWOXPYRZ','NWOWPWRW':'WWWW','NWNXNYNZ':'NNNN','NWNXNYOZ':'NWNXNYOZ','NWOXOYOZ':'NWNXNYOZ','NWOWPXRX':'NWOWPXRX',
'NWOXPWRX':'NWOWPXRX','NWOXPXRW':'NWOWPXRX','NWOWPXPY':'NWOWPXPY','NWOXOYPW':'NWOWPXPY','NWNXOYPY':'NWOWPXPY','NWNXOYPZ':'NWNXOYPZ',
'NWOXOYPZ':'NWNXOYPZ','NWOXPYPZ':'NWNXOYPZ','NWNXOWOY':'NWNXOWOY','NWNXOYOX':'NWNXOWOY','NWNXOXOY':'NWNXOWOY','NWNXOYOW':'NWNXOWOY',
'NWOWPWRX':'NWOWPWRX','NWOWPXRW':'NWOWPWRX','NWOXPXRX':'NWOWPWRX','NWOXPWRW':'NWOWPWRX','NWOWPXRY':'NWOWPXRY','NWOXPYRY':'NWOWPXRY',
'NWOXPYRX':'NWOWPXRY','NWOXPYRW':'NWOWPXRY','NWOXPXRY':'NWOWPXRY','NWOXPWRY':'NWOWPXRY','NWNXOWPX':'NWNXOWPX','NWNXOXPW':'NWNXOWPX',
'NWOXPWPX':'NWNXOWPX','NWOWOXPX':'NWNXOWPX','NWOXPXPW':'NWNXOWPX','NWOXOWPX':'NWNXOWPX','NWNXOWPY':'NWNXOWPY','NWOXPWPY':'NWNXOWPY',
'NWOXOYPX':'NWNXOWPY','NWNXOXPY':'NWNXOWPY','NWOXOYPY':'NWNXOWPY','NWNXOYPX':'NWNXOWPY','NWOXPXPY':'NWNXOWPY','NWOXPYPW':'NWNXOWPY',
'NWOXPYPX':'NWNXOWPY','NWOXOWPY':'NWNXOWPY','NWOWOXPY':'NWNXOWPY','NWNXOYPW':'NWNXOWPY','NWOWOXOY':'NWNNOW','NWNXNYOW':'NWNNOW','NWNXNYOY':'NWNNOW',
'NWOXOYOW':'NWNNOW','NWNXNYOX':'NWNNOW','NWOXOWOY':'NWNNOW','NWOWOXPW':'NWNOWPW','NWOXOWPW':'NWNOWPW','NWOWPWPX':'NWNOWPW','NWNXOWPW':'NWNOWPW',
'NWOWPXPW':'NWNOWPW','NWNXOXPX':'NWNOWPW'}


class ExpressionParser:
    def __init__(self, expList,filterArray):
        self.expList = expList
        self.index = 0

        self.filterArray = filterArray

    def getValue(self):
        value = self.parseExpression()
        return value
    
    #Return the next character
    def next(self):
        try:
            currChar = self.expList[self.index]
            return currChar
            #return self.expList[self.index + 1]
        except:
            return ""

    #Return true/false depending on whether there are still characters
    def hasNext(self):
        return self.index < len(self.expList)
    
    def parseExpression(self):
        return self.parseCommas()
    
    def parseCommas(self):
        cValues = [self.parseColon()]
        
        while True:
            char = self.next()

            if char == ',':
                self.index += 1
                cValues.append(self.parseColon())
            else:
                break

        #c = a.union(*cValues)
        #Comma = 'or', logical_or
        #Can have more than 2 values, will have to loop?
        return np.logical_or.reduce(cValues)
        #return set.union(*cValues)

    def parseColon(self):
        values = [self.parseParenthesis()]
        negValues = []

        while True:
            char = self.next()
            if char == ':':
                self.index += 1
                #valTwo = self.parseParenthesis()
                values.append(self.parseParenthesis())
            elif char == '!':
                self.index += 1
                #valTwo = self.parseParenthesis()
                negValues.append(self.parseParenthesis())
            else:
                break

        # : is 'and', so true values in both arrays - np.logical_and
        allPos = np.logical_and.reduce(values)

        #allPos = set.intersection(*values)

        # ! is 'not', so we want 'and not' those values
        if negValues:
            negValues = [np.logical_not(x) for x in negValues]
            allNeg = np.logical_and.reduce(negValues)
            allPos = np.logical_and(allPos,allNeg)
            
        return allPos
    
    def parseParenthesis(self):
        char = self.next()

        if char == '(':
            self.index += 1
            value = self.parseCommas()
            #if self.next() != ')':
                #raise Exception("No closing parenthesis found at character "+ str(self.index))
            self.index += 1
            return value
        else:
            return self.parseRange()
    
    def parseRange(self):
        char = self.next()

        self.index += 1

        return self.expandRange(char,self.filterArray)


    #Take in a range and an optional startMask
    def expandRange(self, r,startMask=None):
        # Order -
        # Check for %, handle them
        # Check for brackets, handle them   z = re.findall('\[(.+?)\]',test)
        # Check for {}, handle them
        # Check for +, -

        # +
        # -
        # []
        # xxyy
        # RROONN

        #preloadedArrays = ['*']  #,'**','***','****','XXYY','XXYZ','RR','RRON']
        macroList = ['$0G','$1G','$2G','$3B10I','$3B10O','$3B12I','$3B12O','$3B15I','$3B15O','$3B2I','$3B2O','$3B4I',
                     '$3B4O','$3B6I','$3B6O','$3B8I','$3B8O','$4B2','$4B3','$4B4','$4B5','$4B6','$FI12','$FI15',
                     '$FI20','$FI25','$FI30','$FI40','$FI50']


        if r in macroList:
            retSet = loadMask(r, startMask)
            return retSet
        


        #Handle pct - if we have this it's the only value we can have
        if '%' in r:
            retSet = pctHandler(r, startMask)
            #FIXIT - need to account for 5%-10%
            #myR = set(fullList[:pct])
            #return myR
            return retSet

        else:
            #Need to check other conditions

            #Store the sets of possible hand combos here, then run combinatorics at end
            brackCombos = []

            #handle brackets - can have this plus other conditions, need to check for this first
            bracketList = re.findall(r'\[(.+?)\]',r)
            if bracketList:
                for bracketSet in bracketList:
                    listA = bracketHandler(bracketSet)
                    brackCombos.append(listA)

            #Check for {}, handle them
            bracesList = re.findall(r'\{(.+?)\}',r)
            if bracesList:
                pass

            #Check for + outside of braces, and when there are no brackets
            if len(bracketList) == 0 and '+' in r:
                #print("Line 627, in first loop")
                listC = plusHandler(r)
                brackCombos.append(listC)

            elif len(bracketList) == 0 and '-' in r:
                listD = minusHandler(r)
                brackCombos.append(listD)


            #We can set this to whatever characters are left
            plainStr = ''

            #If we have regular characters outside of brackets, or all alone, put them in plainStr
            #Can have [78]J, [78+]J
            #If we have brackets, remove the characters in the brackets (and the brackets)
            if bracketList:
                plainStr = r
                for bracketSet in bracketList:
                    r = r.replace('['+bracketSet+']','')

                    #And also confirm there is no + or - before we know it's a plain string
                    if "+" not in r and "-" not in r:
                        plainStr = cleanString(r)
                
            #If we don't have brackets, confirm no + or - and we know it's a plain string
            elif len(bracketList) == 0:
                if "+" not in r and "-" not in r:
                    plainStr = cleanString(r)

            plainCombos = []
            #If we have any remaining characters, add them to our list
            if len(plainStr) > 0:
                #So plainLists will need to be a list of lists
                plainLists = enumerateHands(plainStr)
                plainCombos += plainLists

            #print(brackCombos,plainCombos)

            retSet = buildMask(brackCombos,plainCombos,startMask)
            
            
            #return retSet
            #return (len(retSet))
            #return retSet.sum()
            return retSet
            '''
            handSet = enumerateHands(allCombos, plainStr)
            return handSet
            '''


def cleanExpression(exp):
    #Get rid of whitespace and capitalize
    myExp = exp.replace(" ", "")
    myExp = myExp.upper()

    #Replace macros
    myExp = myExp.replace('$DS', ':XXYY')
    myExp = myExp.replace('$SS', ':XXYZ')
    myExp = myExp.replace('$NP', '!RR')
    myExp = myExp.replace('$OP', ':RRON')
    myExp = myExp.replace('$TP', ':RROO')
    myExp = myExp.replace('$NT', '!RRR')
    #FIXIT!!  Once we build these arrays, delete and no longer replace these values
    # myExp = myExp.replace('$0G', 'AKQJ-')  #No longer want to replace these values
    # myExp = myExp.replace('$1G', '(AKQT-,AKJT-,AQJT-)')
    # myExp = myExp.replace('$2G', '(AKQ9-,AKT9-,AJT9-)')
    # ##End delete here
    myExp = myExp.replace('$B', '[A-J]')
    myExp = myExp.replace('$M', '[T-7]')
    myExp = myExp.replace('$Z', '[6-2]')
    myExp = myExp.replace('$L', '[A,2,3,4,5,6,7,8]')
    myExp = myExp.replace('$N', '[K-9]')
    myExp = myExp.replace('$F', '[K-J]')
    myExp = myExp.replace('$R', '[A-T]')
    myExp = myExp.replace('$W', '[A,2,3,4,5]')
    #Also don't want to replace $4bFI type macros
    
    #Find commas in between brackets, replace with ;
    bracketList = re.findall(r'\[.+?\]',myExp)
    if bracketList:
        for bracketSet in bracketList:
            #if there's a comma inside of this bracket set
            if ',' in bracketSet:
                #Replace the comma with ; in a temp var
                replaceVar = bracketSet.replace(',',';')
                myExp = myExp.replace(bracketSet, replaceVar)

    return myExp


def chunkExpression(exp):
    retExp = re.findall(r'\(|\)|,|!|\:|[^\(\),!\:]*',exp)
    return retExp[:-1]  #The -1 because there's always an empty list element at the end for some reason




#myFile = np.load('C:/Users/Thomas/Dropbox/Workspace/GTOPoker/rankedHands6maxNum.npy')

def evaluate(expression,board=None,rangeFilter=None):
    #Confirm it's a valid expression
    if sv.confirmExpression(expression):
        #Clean and chunk expression
        expression = cleanExpression(expression)
        expression = chunkExpression(expression)

        #If we have a board, create a numpy mask using this board
        if board is not None:
            rangeFilter = makeBoardMask(board)
        
        p = ExpressionParser(expression,rangeFilter)

        handList = p.getValue()

        cardArray = getCardArray()
        #Want to return both the array and the mask
        return cardArray[handList], handList
    else:
        #FIXIT - do we need to raise an exception here?
        #print("Invalid Hand")
        return False



def makeBoardMask(board):
    '''
    Input is a board string, in format '2H5HTDJC'
    Output is a mask representing the values in our basic hand array that are
    blocked by the cards on this board
    '''
    cardArray = getCardArray()

    board=board.upper()

    #boardVals = [board[i:i+2] for i in range(0, len(board), 2)]
    cardIndexes = ['2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AH',
                   '2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AD',
                   '2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AC',
                   '2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS','AS']

    #[x[i:i+2] for i in range(0, len(x), 2)]  #Splice by 2
    #cardIndexes.index(x)+1  #Just get indexes
    boardVals = [cardIndexes.index(board[i:i+2])+1 for i in range(0, len(board), 2)]

    boardMask=np.zeros((270725,4),dtype=bool)
    for bv in boardVals:

        boardM = cardArray == bv
        boardMask = np.add(boardMask,boardM)

    maskTally = np.sum(boardMask,axis=1)

    retMask = maskTally == 0

    return retMask



############################################
###########################################







###############################################


class Range:
    def __init__(self):
        #Main card array, used several times so make things more effective by loading once
        self.cardArray = getCardArray()






#We'll be passed a string from inside the brackets.  Can be in one of the following formats:
#[As,Js] - only singles allowed, no AsKs, JsTs
#[As-]
#[Jx+]
#[A-T]
def bracketHandler(bString):
    #There can be only one of the above, so we just have to find which one and evaluate it

    #allRanks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    #allSuits = ['C','S','D','H']

    #Handle ',' case - We want to find these and convert to ; in pre-processing
    if ';' in bString:
        sString = bString.split(";")

        ssList = []
        #We want to return from [s,Kc], retrn [*s,Kc]
        for char in sString:

            #If length is 2 we can immediately return values
            if len(char)==2:
                ssList.append(char)
            
            #Otherwise length is 1, we need to see if we have a suit or a rank
            else:

                #This is the case where we have a rank, need to add suit
                if char in ALLRANKS:
                    ssList.append(char+"?")
                #Otherwise it must be a suit
                else:
                    ssList.append("*"+char)
        return ssList

            


    elif '+' in bString:
        retList = plusHandler(bString)
        return retList

    elif '-' in bString:
        retList = minusHandler(bString)
        return retList

    #Final option is that it's just one hand in the brackets
    else:
        #Is either a solitary suit or rank
        #We should check to make sure hand is valid
        if len(bString)==2:
            return [bString]
        
        #Otherwise length is 1, we need to see if we have a suit or a rank
        elif len(bString)==1 and bString in ALLRANKS:
            return [bString+"?"]
        elif len(bString)==1 and bString in ALLSUITS:
            return ["*"+bString]



#Take in a string in any format, 1-8 characters, any combination of suits and ranks.
#Fill in all missing characters with *  and ?
#If 'extend' is True, we'll additional characters to extend it to 8, otherwise leave it as is?
#AKs
#*s
def cleanString(st):
    #Can we create a regEx to pull out each word?
    #handVals = re.findall('[AKQJT98765432RON]?[csdhwxyz]?',st)
    handVals = re.findall('[AKQJT98765432RONP]?[CSDHWXYZ]?',st)
    handVals = handVals[:-1]  #Always has empty value at end for some reason

    myHandList = []

    #Figure out if we have a rank, a suit, or both
    for hv in handVals:
        if len(hv) == 2:
            myHandList.append(hv)
        elif len(hv) == 1:
            if hv in ALLRANKS or hv in ALLRANKVARS:
                myHandList.append(hv+"?")
            else:
                myHandList.append("*"+hv)

    return ''.join([x for x in myHandList])




def plusHandler(pString):
    '''
    Input is some string containing a +, such as 55+, 7s8s+
    Output is an enumerated list of the matches for this range, such as 55, 66, 77, etc

    Will only be a single string with a single +, multiple would be separated in different brackets
    '''
    #Increment each card in the list by 1 until we have a value equal to A
    convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
    bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}

    #First we need to clean the data, either confirm suits are there or add suits
    pString = pString[:pString.find('+')]
    pString = cleanString(pString)

    #List to append our values to which we will return
    retList = []

    #convert card values to numbers and create a new list
    pString2Nums = list(pString[0::2])
    pString2Nums = [convDict[x] for x in pString2Nums]

    #Now loop through and append each one to our list
    #5d6x7y
    while max(pString2Nums) <= 13:
        #Convert back to a string - first get the letters back
        pStringS = [bConvDict[x] for x in pString2Nums]
        
        #Create a string with the suits and append it
        retList.append(''.join(pStringS[int(index/2)] if index % 2 == 0 else char for index, char in enumerate(pString)))

        #Increment by one and continue looping
        pString2Nums = [x+1 for x in pString2Nums]

    #print(retList)
    return retList


#Convert any sequence with a - in it.  Can decrease all the way to 2, or to a certain range
#5-
#5s6s-
#J-5
def minusHandler(mString):
    #Decrease each card in the list by 1 until we have a value equal to A
    convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
    bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}
    
    #First we need to clean the data, either confirm suits are there or add suits
    mString = mString.split("-")  #Returns a LIST!

    #Get our basic string for the starting range
    mStringA = cleanString(mString[0])

    #convert card values to numbers and create a new list
    mStringA2Nums = list(mStringA[0::2])
    mStringA2Nums = [convDict[x] for x in mStringA2Nums]

    mStringB2Nums = [1 for x in mStringA2Nums]

    #print(mStringA)
    #Two cases, the straight -, and the -range
    #This is the -range case.  We need to set the second string, and convert it to a list
    if len(mString[1]) > 0:
        mStringB = cleanString(mString[1])
        mStringB2Nums = list(mStringB[0::2])
        mStringB2Nums = [convDict[x] for x in mStringB2Nums]


    #List to append our values to which we will return
    retList = []


    #Now loop through and append each one to our list
    #5d6x7y
    nList=[]
    while nList != mStringB2Nums:
        #Convert back to a string - first get the letters back
        mStringS = [bConvDict[x] for x in mStringA2Nums]
        #Create a string with the suits and append it
        retList.append(''.join(mStringS[int(index/2)] if index % 2 == 0 else char for index, char in enumerate(mStringA)))

        #ugly temporary variable so we still the final loop in
        nList = mStringA2Nums
        tempL = []

        #Check for second condition where we'd break the loop - min value of 1 and no ending values
        if len(mString[1])==0 and min(mStringA2Nums)==1:
            break


        #Transform each element one step closer to the corresponding element in the matching array
        for mI,mChar in enumerate(mStringA2Nums):
            #We want to append -1 by the distance
            if mChar>mStringB2Nums[mI]:
                tempL.append(mChar-1)
            elif mChar<mStringB2Nums[mI]:
                tempL.append(mChar+1)
            else:
                tempL.append(mChar)

        mStringA2Nums = tempL


    '''
    while min(mStringA2Nums) >= min(mStringB2Nums):

        #Convert back to a string - first get the letters back
        mStringS = [bConvDict[x] for x in mStringA2Nums]
        #Create a string with the suits and append it
        retList.append(''.join(mStringS[int(index/2)] if index % 2 == 0 else char for index, char in enumerate(mStringA)))

        #Increment by one and continue looping
        mStringA2Nums = [x-1 for x in mStringA2Nums]
    '''


    return retList



#Return a list of lists of whatever characters are left over
def enumerateHands(plainStr):
    #Split our hands into separate values in a string
    handVals = re.findall('[AKQJT98765432RONP]?[CSDHWXYZ]?',plainStr)
    handVals = handVals[:-1]  #Always has empty value at end for some reason

    finalVals = [[x] for x in handVals if len(x)==2]

    #Pull out values that need to be modified
    modVals = [x for x in handVals if len(x)==1]
    
    #Modify ones containing just a suit
    appVals1 = [[x+"?"] for x in modVals if x in ALLRANKS or x in ALLRANKVARS]

    #Modify ones containing just a rank
    appVals2 = [["*"+x] for x in modVals if x in ALLSUITS or x in ALLSUITVARS]

    #Finally combine all the lists
    finalVals = finalVals + appVals1 + appVals2
    return finalVals



def findPatternSimple(hand='AcQhJsTd'):
    #h = hand.upper()
    ranks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2','R','O','N','P']
    suits = ['C','S','D','H','W','X','Y','Z']

    hvList = hand

    #indCounts = [h.count(x) for x in h]
    #Want to get rid of all W, X, RX, etc hands.  RR/OO ok I guess.
    if len(hvList)>1:

        #Just do one sort?
        rankSorted=sorted(hvList)
        #print(rankSorted)
        #And now replace all the letters.  Make them all lowercase,
        rankSorted=[x.lower() for x in rankSorted]

        #Now need some way of iterating over it and changing these values
        reassembled = "".join(rankSorted)
        #print(reassembled)
        rankVars = ['N','O','P','R']
        suitVars = ['W','X','Y','Z']

        rvI = 0
        svI = 0
        replaceRanks = ['a','k','q','j','t','9','8','7','6','5','4','3','2','r','o','n','p']
        replaceSuits = ['c','s','d','h','w','x','y','z']

        i=0

        #while len(rankSet)>0 or len(suitSet)>0:  #and i<len(reassembled):
        for i in range(len(reassembled)):
            #print("lengths are",len(rankSet),len(suitSet))

            myChar = reassembled[i]
            #print("myChar is",myChar)

            if myChar in replaceRanks:
                #If it's in our list of unused ranks, replace all those values
                reassembled = reassembled.replace(myChar,rankVars[rvI])
                #Increase are rankVarIndex
                rvI += 1
                #print("RVI",rvI)

            elif myChar in replaceSuits:
                #If it's in our list of unused suits, replace all those values
                reassembled = reassembled.replace(myChar,suitVars[svI])
                #print("replacing",reassembled)
                #Increase are rankVarIndex
                svI += 1
        #Want to remove ? and * from reassembled.  Can we always remove the *?
        #KJ*cc - definitely not KJxx.  possible problem here
        #KJxx and KJ*xx are different.  We only need to keep the * if it is following
        #a rank.  So remove all the ones that follow a suit

        #Finally we can remove any * that follows a suit
        #Suits are WXYZ
        if '*' in reassembled:
            #If the first value is a '*', we have no ranks, remove all the *
            if reassembled[0]=='*':
                reassembled = reassembled[1:]
        
            #Replace all the pairs where we don't need it
            reassembled=reassembled.replace('W*','W').replace('X*','X').replace('Y*','Y').replace('Z*','Z')
            #.replace('?*','*') replace with '*' - don't need this, we'll remove the ? later anyway.

        #We can safely remove the any suit var, ?
        reassembled = reassembled.replace('?','')
        

        return reassembled
    #If it's length one all hands are possible, what should we return?
    else:
        return None


def getCardArray():
    '''
    Return numpy array containing our ordered list of hands
    '''
    return np.load(ploDir+'npfiles/pptRankedHUnums.npy')



#Takes in a list of list of possible hands, returns a numpy mask of the hands that are possible
def buildMask(brackCombos,plainCombos,startMask):

    #cardArray = np.load('C:/Users/Thomas/Dropbox/Workspace/GTOPoker/rankedHandsHUNum.npy')
    cardArray = getCardArray()

    #All combos is a list of lists, can contain from 1 to 4 cards that we must match
    possArrays = [(1,2,3),(1,2,4),(1,2,5),(1,2,6)]
    handArry = None

    #allRanks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    #allSuits = ['C','S','D','H']
    #rList = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    #rvList = ['R','O','N','P']
    #sList = ['C','S','D','H']
    #svList = ['W','X','Y','Z']
    useRIDict = {'R':[],'O':[],'N':[],'P':[]}  #{R:[1,2] , O:[3]}
    useSIDict = {'W':[],'X':[],'Y':[],'Z':[]}


    #print(brackCombos,plainCombos)


    #Process -
    #1. Apply our conversion pattern Simple function to find the pattern
    #2. Search the dictionary for this pattern, find the file to load and load it
    #3. Determine if we have specific hands that we want to filter for, and if so do it.
    #4. Return a MASK, a full 275k length mask which we'll be able to use above to filter for hands

    #Join the individual list elements
    plainCombos = ["".join(x) for x in plainCombos]
    #Now convert them to one string
    plainCombos = "".join(plainCombos)

    #print("Starting",brackCombos, plainCombos)
    #Add this to our list of brackCombos, so our itertools operation will work
    #fullCombos = brackCombos+[plainCombos]
    
    fullCombos=brackCombos.copy()
    fullCombos.append([plainCombos])

    #print("FullCombos",fullCombos)
    #fullCombos.append([plainCombos])

    #brackCombos.append([plainCombos])
    #print("B, then f",brackCombos,fullCombos)
    #print(fullCombos)

    

    #brackCombos

    #print(fullCombos)

    comboList = list(itertools.product(*fullCombos))
    #COmbine the tuples
    comboList = ["".join(x) for x in comboList]
    #Separate out the hands again


    iterateList = []
    for c in comboList:
        cl = [c[i:i+2] for i in range(0,len(c),2)]
        iterateList.append(cl)


    #print(iterateList)

    #Combine the lists of lists
    #fullList = brackCombos + plainCombos
    #fullList = [x[0] for x in fullList]

    masterMask = np.zeros(270725,dtype='bool')

    plainRIndex = []
    #print("BrackCombos",brackCombos)
    #Check to see if we need to handle [Ak-]RR type hands
    if len(brackCombos)>0 and any(x[0] in ['R','O','N','P'] for x in plainCombos):
        #Just want to record the index values here, then we can strip them all later
        for charI,char in enumerate(comboList[0]):
            if char in ['R','O','N','P']:
                plainRIndex.append(charI)

    for subHand in iterateList:

        #print(fullList)
        if len(subHand)>1:
            #Need to get pattern WITHOUT RRON if we have those outside of brackets
            if len(plainRIndex)>0:
                #1. Apply our conversion patternSimple function to find the pattern
                #We want to strip all RONs that are in plainCombos from this mask
                #Actually this is easy!  We know there can't be any RONs in the brackets
                #So just remove them all, and record their index values
                #print(subHand)
                subHandCleaned = [x.replace("R","*").replace("O","*").replace("N","*").replace("P","*") for x in subHand]
                subHandCleaned = [x for x in subHandCleaned if x!='*?']
                myPattern = findPatternSimple(subHandCleaned)
            else:
                #1. Apply our conversion patternSimple function to find the pattern
                myPattern = findPatternSimple(subHand)

            #2. Search the dictionary for this pattern, find the file to load and load it
            #myPattern will be a string
            myPattern = patternDict[myPattern]
            #FIXIT - want os.curr path here
            parMask = np.load(ploDir+'npfiles/'+myPattern+'.npy')


        else:
            parMask = np.ones(270725,dtype='bool')

        #print(myPattern, parMask.sum())

        #If we included a starting range mask, combine these two masks
        if startMask is not None:
            #print("Integrating start mask")
            parMask = np.logical_and(parMask,startMask)


        #3. Determine if we have specific hands that we want to filter for, and if so do it.
        realCards = ['2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AH',
                     '2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AD',
                     '2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AC',
                     '2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS','AS',
                     'A?','K?','Q?','J?','T?','9?','8?','7?','6?','5?','4?','3?','2?',
                     '*C','*D','*S','*H']
        varCards = ['R','O','N','P','W','X','Y','Z','*','?']

        
        #All constants
        if all(x in realCards for x in subHand):
            #If this is true, we need to run the filter.  Confirm all values are separate values in this list
            parMask = maskConstants(cardArray,parMask,subHand,realCards)
            
            #FIXIT - we have problems with certain hands like JT9*c, at some point we should precisely describe where this fails

            #Greater than length 2 - J*c is ok
            #At least one undefined var of each kind, so one * and one ?
            if len(subHand) >=3 and any('*' in x for x in subHand) and any('?' in x for x in subHand):

                #Check for at least two unique vars or sets?
                if len(set([x for x in subHand if '*' in x]))>1 or len(set([x for x in subHand if '?' in x]))>1:

                    strArray = np.load(ploDir+'npfiles/pptRankedHUstrs.npy')
                    strArray = strArray[parMask]

                    fullCheckMask = rowCheck(strArray,subHand)

                    parMask[parMask] = fullCheckMask


        
        #All vars - mask already gives us hand
        elif all(x[0] in varCards for x in subHand) and all(x[1] in varCards for x in subHand):
            pass

        #Final case - mix of constants and vars
        else:
            #print("Before",np.sum(parMask))
            #First reduce hand with the constants we have
            if len(plainRIndex)==0:
                parMask = maskConstantsWithVars(cardArray,parMask,subHand,realCards)
            
                #currTotal = np.sum(parMask)
                #print("Second",np.sum(parMask))
                parMask = step2VarMatching(cardArray,parMask,subHand,realCards)
                #print("Third",np.sum(parMask))

                #if np.sum(parMask) != currTotal:
                    #print("New total",subHand)

            #Want to remove this - only check if necessary
            if True:

                strArray = np.load(ploDir+'npfiles/pptRankedHUstrs.npy')
                strArray = strArray[parMask]

                fullCheckMask = rowCheck(strArray,subHand,plainRIndex)

                parMask[parMask] = fullCheckMask
        
        #Now we've modified our parMask to be correct in the case of individual values, we can return it
        masterMask = np.logical_or(masterMask,parMask)

    return masterMask




def pctHandler(r, startMask):
    '''
    Inputs: r is a string of a percentage
    Four cases - 3%, 3%6h, 30%-50%, 30%-50%6h

    startMask is an optional parameter of hands that are known to be impossible

    Returns array with the hands represented by this string
    '''
    
    pctMask = np.zeros(270725,dtype='bool')

    if '6H' in r:
        #parMask = np.load(ploDir+'/npfiles/'+myPattern+'.npy')
        orderedList = np.load(ploDir+'npfiles/pptRanked6maxMap.npy')
        sIndexes = [0, 2700, 5400, 8118, 10818, 13536, 16224, 18948, 21648, 
                    24344, 27072, 29772, 32486, 35188, 37900, 40608, 43308, 
                    46008, 48726, 51416, 54140, 56842, 59558, 62266, 64960, 
                    67672, 70386, 73090, 75798, 78492, 81206, 83916, 86614, 
                    89320, 92040, 94732, 97452, 100148, 102864, 105564, 108284,
                    110990, 113699, 116405, 119115, 121817, 124521, 127229, 
                    129937, 132639, 135351, 138059, 140775, 143483, 146189, 
                    148887, 151599, 154295, 157007, 159711, 162421, 165125, 
                    167833, 170549, 173245, 175959, 178675, 181385, 184093, 
                    186781, 189507, 192199, 194915, 197607, 200327, 203035, 
                    205751, 208449, 211151, 213865, 216571, 219277, 221979, 
                    224695, 227403, 230093, 232813, 235525, 238231, 240935, 
                    243639, 246339, 249059, 251757, 254465, 257185, 259889, 
                    262589, 265305, 268014, 270725]

    else:
        #Don't actually need to load the hand rankings otherwise
        #orderedList = np.load('C:/Users/Thomas/Dropbox/Workspace/GTOPoker/ArrayCalcsSets/rankedHU.npy')
        sIndexes = [0, 2688, 5412, 8112, 10806, 13518, 16234, 18942, 21654, 
                    24346, 27068, 29762, 32466, 35188, 37892, 40600, 43312, 
                    46022, 48724, 51430, 54144, 56846, 59548, 62248, 64966, 
                    67676, 70382, 73088, 75792, 78492, 81198, 83903, 86611, 
                    89323, 92041, 94739, 97449, 100149, 102865, 105559, 108289,
                    110985, 113685, 116389, 119101, 121821, 124525, 127237, 
                    129927, 132643, 135341, 138059, 140767, 143479, 146183, 
                    148883, 151603, 154293, 157013, 159713, 162423, 165133, 
                    167833, 170553, 173257, 175961, 178655, 181379, 184083, 
                    186797, 189507, 192213, 194921, 197627, 200327, 203041, 
                    205733, 208441, 211151, 213859, 216561, 219283, 221985, 
                    224687, 227391, 230115, 232819, 235523, 238229, 240939, 
                    243651, 246347, 249057, 251769, 254469, 257169, 259885, 
                    262597, 265309, 268001, 270725]

    if '-' in r:
        pcts = re.findall(r'(\d{1,3})%',r)

        pcts = [int(x) for x in pcts]
        #We'll always have two values, want to subtract 1 from the lower one to do it PPT style
        index1 = sIndexes[min(pcts)-1]
        index2 = sIndexes[max(pcts)]

        #If it's 6max, we have to apply the mask indirectly - to the numbers
        if '6H' in r:
            #FIXIT-FIXING HERE
            sixConvMask = orderedList[index1:index2]
            #sixConvMask = (orderedList>=index1) & (orderedList<index2)
            pctMask[sixConvMask] = True

        else:
            pctMask[index1:index2]=True

        #slice1 = orderedList[:index1]
        #slice2 = orderedList[:index2]

        #print(len(slice1))
        #print(len(slice2))
        #The slice we return will be slice2 - slice1, 50-70% is the hands between the top 50 and top 70
        #Actually order doesn't matter, we just want to do an interesection?

        #retuSet = set(slice1).symmetric_difference(set(slice2))


    else:
        #Find 1-3 characters for the percentage, immediately preceding '%'
        pct = re.findall(r'(\d{1,3})%',r)
        #print(pct[0])
        #print(int(pct[0])/100*270725)
        index = sIndexes[int(pct[0])]
        #print("Index",index)
        #print("length of straightList",len(orderedList))
        #retuSet = orderedList[:index]
        #retuSet = set(retuSet)
        if '6H' in r:
            #sixConvMask = orderedList<index
            sixConvMask = orderedList[:index]
            #sixConvMask = (orderedList>=index1) & (orderedList<index2)
            pctMask[sixConvMask] = True

        else:
            pctMask[:index]=True

    # retuSet = [x.upper() for x in retuSet]
    # retuSet = [sorted((x[i:i+2]) for i in range(0, len(x), 2)) for x in retuSet]
    # retuSet = ["".join(x) for x in retuSet]
    # retuSet = set(retuSet)
    #print("length",len(retuSet))
    if startMask is not None:
        pctMask = np.logical_and(pctMask,startMask)

    return pctMask




def loadMask(myMacro, startMask):

    # #First get the value we're going to refer to all identical lookups by
    # macroList = ['$0G','$1G','$2G','$3B10I','$3B10O','$3B12I','$3B12O','$3B15I','$3B15O','$3B2I','$3B2O','$3B4I',
    #                  '$3B4O','$3B6I','$3B6O','$3B8I','$3B8O','$4B2','$4B3','$4B4','$4B5','$4B6','$FI12','$FI15',
    #                  '$FI20','$FI25','$FI30','$FI40','$FI50']

    myMask = np.load(ploDir+'npfiles/'+myMacro+'.npy')

    if startMask is not None:
        return np.logical_and(myMask,startMask)

    return myMask


    
    
    #Currently not adding masks for -
    # '$B', '[A-J]'
    # '$M', '[T-7]'
    # '$Z', '[6-2]'
    # '$L', '[A,2,3,4,5,6,7,8]'
    # '$N', '[K-9]'
    # '$F', '[K-J]'
    # '$R', '[A-T]'
    # '$W', '[A,2,3,4,5]'

    #Here are the hand ranges these correspond to
    #('$0G', 'AKQJ-')
    #('$1G', '(AKQT-,AKJT-,AQJT-)')
    #('$2G', '(AKQ9-,AKT9-,AJT9-)')
    # 3B10I,"(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:16%6h,xxyz:12%6h),Axxy!RR:(xxyy:18%6h),*!RR![6-]:(xxyy:12%6h,xxyy!A),OORR:xxy,$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy:30%6h,xxyz:12%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy:18%6h,xxyz:10%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:16%6h),(KQ9-,KJ9-)!RR:(xxyy:12%6h),(4556+,4456+,6654+):(xxyy:18%6h,xxyz:12%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:14%6h,xxyz:12%6h))$nt",,yes,
    # 3B10O,"(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64,KT-74):xxy, KK:(3%6h,xxyy,AQ,QJ-65,QT-64):xxy, QQ:xxyy, JJ:(xxyy:6%6h,xxyy!A:8%6h), AK!RR:xxyy, Axxy!RR:(xxyy:12%6h,xxyz:10%6h), *!RR![6-]:xxyy, OORR:(xxyy,xxyz:45%6h), $0G:60%6h, $1G:(xxyy:55%6h,xxyz:55%6h,xxy:45%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:24%,xxyz:16%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:18%6h,xxyz:12%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:18%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:12%6h,Axxyy:20%6h), (4556+,4456+,6654+):(xxyy:16%6h,xxyz:14%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:14%6h,xxyz:12%6h))$nt",,yes,
    # 3B12I,"(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy,xxyz:16%6h),Axxy!RR:(xxyy:26%6h),*!RR![6-]:(xxyy,xxy:10%6h),OORR:xxy,$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy,xxy:20%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy:24%6h,xxy:12%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:20%6h),(KQ9-,KJ9-)!RR:(xxyy:16%6h),(4556+,4456+,6654+):(xxyy,xxyz:20%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy,xxyz:18%6h))$nt",,yes,
    # 3B12O,"(*!RRR:2%6h, AA:xxy, KK:(4%6h,xxyy,AQ,QJ-65,QT-64):xxy, QQ:xxyy, JJ:(xxyy:6%6h,xxyy!A:8%6h), AK!RR:(xxyy,xxyz:12%6h), Axxy!RR:(xxyy:15%6h,xxyz:12%6h), *!RR![6-]:(xxyy,xxyz:12%6h), OORR:(xxyy,xxyz:50%6h), $0G:60%6h, $1G:(xxyy:55%6h,xxyz:55%6h,xxy:45%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:40%6h,xxyz:20%6h,xxy:15%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:30%6h,xxyz:20%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:24%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:18%6h,Axxyy:20%6h), (4556+,4456+,6654+):(xxyy:22%6h,xxyz:18%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:18%6h,xxyz:16%6h))$nt",,yes,
    # 3B15I,"(*!RRR:3%6h,AA:xxy,KK:4%6h,QQ:(xxyy:2%6h,xxyy!A:6%6h),JJ:(xxyy:4%6h,xxyy!A:8%6h),AK!RR:(xxyy,xxyz:16%6h),Axxy!RR:(xxyy,xxyz:16%6h),*!RR![6-]:(xxyy,xxyz:14%6h),OORR,$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy,xxy:24%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy,xxy:16%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:34%6h),(KQ9-,KJ9-)!RR:(xxyy:32%6h),(4556+,4456+,6654+):(xxyy,xxyz:28%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy,xxyz:22%6h))$nt",,yes,
    # 3B15O,"(*!RRR:2%6h, AA:(xxy,JT+), KK:(xxy,AQ), QQ:xxyy, JJ:xxyy, AK!RR:(xxyy,xxy:14%6h), Axxy!RR:(xxyy:15%6h,xxy:15%6h), *!RR![6-]:(xxyy,xxy:18%6h), OORR, $0G:60%6h, $1G:(xxyy:55%6h,xxyz:55%6h,xxy:45%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:40%6h,xxyz:30%6h,xxy:25%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:30%6h,xxyz:25%6h,xxy:15%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:20%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:20%6h,Axxyy:20%6h), (4556+,4456+,6654+):(xxyy:30%6h,xxyz:24%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:24%6h,xxyz:20%6h))$nt",,yes,
    # 3B2I,"(*!RRR:1%6h,AA:(xxyy,56+,46+):xxy,KK:2%6h,QQ:2%6h,JJ:3%6h,AK!RR:3%6h,Axxy!RR:3%6h,*!RR![6-]:3%6h,OORR:(8%6h!JJ+),$0G:(xxyy:30%6h),$1G:(xxyy:26%6h))$nt",,yes,
    # 3B2O,"(*!RRR:1%6h,AA:(xxyy,56+,46+):xxy,KK:2%6h,QQ:2%6h,JJ:3%6h,AK!RR:3%6h,Axxy!RR:3%6h,*!RR![6-]:3%6h,OORR:(8%6h!JJ+),$0G:(xxyy:30%6h),$1G:(xxyy:26%6h))$nt",,yes,
    # 3B4I,"(*!RRR:2%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:4%6h),Axxy!RR:(xxyy:4%6h),*!RR![6-]:(xxyy:4%6h,xxyy!A),OORR:(xxyy:20%6h!JJ+),$0G:(xxyy:42%6h),$1G:(xxyy:30%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:8%6h),(KQ9-,KJ9-)!RR:(xxyy:6%6h),(4556+,4456+,6654+):(xxyy:10%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:10%6h))$nt",,yes,
    # 3B4O,"(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64):xxy, KK:2%6h, QQ:(xxyy:2%6h,xxyy!A:4%6h), JJ:(xxyy:4%6h,xxyy!A:6%6h), AK!RR:(xxyy:4%6h), Axxy!RR:(xxyy:4%6h), *!RR![6-]:(xxyy:6%6h,xxyy!A), OORR:(xxyy:20%6h!JJ+), $0G:(xxyy:50%6h, xxyz:45%6h), $1G:(xxyy:30%6h, xxyz:20%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:10%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:8%6h), (KQ9-,KJ9-)!RR:(xxyy:6%6h), (4556+,4456+,6654+):(xxyy:8%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:6%6h))$nt",,yes,
    # 3B6I,"(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:6%6h),Axxy!RR:(xxyy:6%6h),*!RR![6-]:(xxyy:6%6h,xxyy!A),OORR:((xxyy:40%6h,xxyz:20%6h)!JJ+),$0G:(xxyy,xxyz:60%6h),$1G:(xxyy:30%6h,xxyz:50%6h),(AQT9-, AKJ9-, AQJ9-):(xxyy:20%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:10%6h),(KQ9-,KJ9-)!RR:(xxyy:8%6h),(4556+,4456+,6654+):(xxyy:15%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:10%6h))$nt",,yes,
    # 3B6O,"(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64,KT-74):xxy, KK:(2%6h,xxyy), QQ:(xxyy:2%6h,xxyy!A:4%6h), JJ:(xxyy:4%6h,xxyy!A:6%6h), AK!RR:(xxyy:6%6h), Axxy!RR:(xxyy:6%6h), *!RR![6-]:(xxyy,xxyy!A), OORR:((xxyy,xxyz:25%6h)!JJ+), $0G:(xxyy:50%6h, xxyz:50%6h), $1G:(xxyy:30%6h,xxyz:50%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:16%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:8%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:12%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:8%6h,Axxyy:16%6h), (4556+,4456+,6654+):(xxyy:12%6h,xxyz:10%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:10%6h,xxyz:8%6h))$nt",,yes,
    # 3B8I,"(*!RRR:3%6h,AA:(2%6h,xxy),KK:3%6h,QQ:(xxyy:2%6h,xxyy!A:4%6h),JJ:(xxyy:4%6h,xxyy!A:6%6h),AK!RR:(xxyy:12%6h),Axxy!RR:(xxyy:10%6h),*!RR![6-]:(xxyy:8%6h,xxyy!A),OORR:((xxyy,xxyz:30%6h)!JJ+),$0G:50%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):(xxyy:24%6h),(AKJ8-, AQ98-, AQJ8-):(xxyy:16%6h),(KQJ-,KQT-,KJT-)!RR:(xxyy:15%6h),(KQ9-,KJ9-)!RR:(xxyy:12%6h),(4556+,4456+,6654+):(xxyy:18%6h,xxyz:10%6h),(3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:12%6h,xxyz:10%6h))$nt",,yes,
    # 3B8O,"(*!RRR:2%6h, AA:(xxyy,KQ-65,KJ-64,KT-74):xxy, KK:(2%6h,xxyy,AQ,QJ-98):xxy, QQ:xxyy, JJ:(xxyy:6%6h,xxyy!A:8%6h), AK!RR:(xxyy:8%6h), Axxy!RR:(xxyy:10%6h), *!RR![6-]:xxyy, OORR:((xxyy,xxyz:50%6h)!QQ+), $0G:60%6h, $1G:(xxyy:42%6h,xxyz:50%6h), (AQT9-, AKJ9-, AQJ9-):(xxyy:20%,xxyz:10%6h), (AKJ8-, AQ98-, AQJ8-):(xxyy:16%6h,xxyz:10%6h), (KQJ-,KQT-,KJT-)!RR:(xxyy:16%6h,Axxyy:20%6h), (KQ9-,KJ9-)!RR:(xxyy:8%6h,Axxyy:16%6h), (4556+,4456+,6654+):(xxyy:14%6h,xxyz:12%6h), (3556+,4457+,4476+,4463+,6643+,6653+):(xxyy:12%6h,xxyz:10%6h))$nt",,yes,
    # 4B2,"(AA:2%6h,AK!RR:3%6h,(OORR)!(JJ+):4%6h,$0G:10%6h)$nt",,yes,
    # 4B3,"(AA:3%6h, AKK:3%6h, AK!RR:3%6h, (OORR)!(JJ+):4%6h, $0G:12%6h, $1G:7%6h)$nt",,yes,
    # 4B4,"(AA, AKK:4%, KK:3%, AQQ:2%, AK!RR:5%, (OORR)!(JJ+):5%, $0G:17%, $0G![J+]:24%, $1G:8%, $1G![J+]:12%, (AQT9-, AKJ9-, AQJ9-):4%, (AKJ8-, AQ98-, AQJ8-):4%)$nt",,yes,
    # 4B5,"(AA, AKK:5%, KK:4%, AQQ:3%, AK!RR:6%, (OORR)!(JJ+):6%, $0G:21%, $0G![J+]:30%, $1G:11%, $1G![J+]:16%, (AQT9-, AKJ9-, AQJ9-):6%, (AKJ8-, AQ98-, AQJ8-):6%)$nt",,yes,
    # 4B6,"(AA, AKK:6%, KK:5%, AQQ:3%, AK!RR:7%, (OORR)!(JJ+):8%, $0G:30%, $0G![J+]:42%, $1G:16%, $1G![J+]:20%, (AQT9-, AKJ9-, AQJ9-):8%, (AKJ8-, AQ98-, AQJ8-):8%)$nt",,yes,
    # FI12,"(*!RRR:8%6h,AA:8%6h,KK:6%6h,QQ:7%6h,JJ:6%6h,AK!RR:7%6h,Axxy!RR:13%6h,*!RR![6-]:8%6h,OORR:(20%6h!JJ+),$0G:50%6h,$1G:28%6h,(AQT9-, AKJ9-, AQJ9-):21%6h,(AKJ8-, AQ98-, AQJ8-):10%6h,(KQJ-,KQT-,KJT-)!RR:10%6h,(KQ9-,KJ9-)!RR:8%6h,(4556+,4456+,6654+):25%6h,(3556+,4457+,4476+,4463+,6643+,6653+):16%6h)$nt",,yes,
    # FI15,"(*!RRR:10%6h,AA:10%6h,KK:9%6h,QQ:10%6h,JJ:9%6h,AK!RR:10%6h,Axxy!RR:16%6h,*!RR![6-]:13%6h,OORR:(25%6h!JJ+),$0G:60%6h,$1G:34%6h,(AQT9-, AKJ9-, AQJ9-):25%6h,(AKJ8-, AQ98-, AQJ8-):14%6h,(KQJ-,KQT-,KJT-)!RR:14%6h,(KQ9-,KJ9-)!RR:10%6h,(4556+,4456+,6654+):30%6h,(3556+,4457+,4476+,4463+,6643+,6653+):20%6h)$nt",,yes,
    # FI20,"(*!RRR:14%6h,AA:16%6h,KK:14%6h,QQ:15%6h,JJ:14%6h,AK!RR:14%6h,Axxy!RR:23%6h,*!RR![6-]:20%6h,OORR:(35%6h!JJ+),$0G:60%6h,$1G:40%6h,(AQT9-, AKJ9-, AQJ9-):34%6h,(AKJ8-, AQ98-, AQJ8-):21%6h,(KQJ-,KQT-,KJT-)!RR:20%6h,(KQ9-,KJ9-)!RR:16%6h,(4556+,4456+,6654+):40%6h,(3556+,4457+,4476+,4463+,6643+,6653+):23%6h)$nt",,yes,
    # FI25,"(*!RRR:18%6h,AA:20%6h,KK:18%6h,QQ:19%6h,JJ:19%6h,AK!RR:19%6h,Axxy!RR:30%6h,*!RR![6-]:25%6h,OORR:(45%6h!JJ+),$0G:70%6h,$1G:50%6h,(AQT9-, AKJ9-, AQJ9-):42%6h,(AKJ8-, AQ98-, AQJ8-):25%6h,(KQJ-,KQT-,KJT-)!RR:24%6h,(KQ9-,KJ9-)!RR:20%6h,(4556+,4456+,6654+):50%6h,(3556+,4457+,4476+,4463+,6643+,6653+):28%6h)$nt",,yes,
    # FI30,"(*!RRR:22%6h,AA:24%6h,KK:22%6h,QQ:24%6h,JJ:24%6h,AK!RR:25%6h,Axxy!RR:37%6h,*!RR![6-]:30%6h,OORR:(55%6h!QQ+),$0G:80%6h,$1G:60%6h,(AQT9-, AKJ9-, AQJ9-):49%6h,(AKJ8-, AQ98-, AQJ8-):30%6h,(KQJ-,KQT-,KJT-)!RR:30%6h,(KQ9-,KJ9-)!RR:24%6h,(4556+,4456+,6654+):60%6h,(3556+,4457+,4476+,4463+,6643+,6653+):36%6h)!kkk",,yes,
    # FI40,"(*!RRR:32%6h,AA:40%6h,KK:36%6h,QQ:36%6h,JJ:36%6h,AK!RR:36%6h,Axxy!RR:56%6h,*!RR![6-]:40%6h,OORR:75%6h,$0G:90%6h,$1G:80%6h,(AQT9-, AKJ9-, AQJ9-):64%6h,(AKJ8-, AQ98-, AQJ8-):40%6h,(KQJ-,KQT-,KJT-)!RR:40%6h,(KQ9-,KJ9-)!RR:32%6h,(4556+,4456+,6654+):80%6h,(3556+,4457+,4476+,4463+,6643+,6653+):47%6h)!kkk-",,yes,
    # FI50,"(*!RRR:40%6h,AA,KK,QQ:50%6h,JJ:50%6h,AK!RR:50%6h,Axxy!RR:66%6h,*!RR![6-]:50%6h,OORR,$0G,$1G,(AQT9-, AKJ9-, AQJ9-):74%6h,(AKJ8-, AQ98-, AQJ8-):64%6h,(KQJ-,KQT-,KJT-)!RR:60%6h,(KQ9-,KJ9-)!RR:50%6h,(4556+,4456+,6654+),(3556+,4457+,4476+,4463+,6643+,6653+):52%6h)!kkk-",,yes,


    #So use itertools to generate lists of all combinations of these ones








################################  RIVER HANDLER ##########################

#Takes in an expression and enumerates all the possible rivers it represents
# A
# s
# As
# A-5
# As-5s
# Ts-
# Ts+
def expandRivers(exp):
    exp = exp.upper()
    exp = exp.split(",")

    cardIndexes = ['2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AH',
                   '2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AD',
                   '2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AC',
                   '2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS','AS']
    convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
    bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}

    rivList = []
    #So now we've split it up and we know we have valid syntax, go through each expression and add those values to our list
    for subExp in exp:

        # A-5
        # As-5s
        # Ts-
        if '-' in subExp:
            #We want expression to work both ways
            #A-5 or 5-A both ok

            #So one way to do it would be to evaluate both separately, then take the values in one set but not the other
            
            subExpSplit = subExp.split("-")  #['Jc', ''], or ['T', '5']

            highCard = subExpSplit[0]  #Will be 'JC' or 'J'
            #Look up the first value of this (because it must be a rank)
            cardVal = convDict[highCard[0]]
            #Get all the values equal to or greater than this value
            fullVals = list(range(1,cardVal+1))
            #Convert ints back to strs
            strFullVals = [bConvDict[x] for x in fullVals]
            #Get all the cards which match any of these values
            matchList = [x for x in cardIndexes if any(y in strFullVals for y in x)]
            #If we have a suit, restrict match list
            if len(highCard) == 2:
                matchList = [x for x in matchList if highCard[1] in x]
            
        
            highCard2 = subExpSplit[1]
            if len(highCard2) > 0:
                #Look up the first value of this (because it must be a rank)
                cardVal = convDict[highCard2[0]]
                #Get all the values equal to or greater than this value
                fullVals = list(range(1,cardVal+1))
                #Convert ints back to strs
                strFullVals = [bConvDict[x] for x in fullVals]
                #Get all the cards which match any of these values
                matchList2 = [x for x in cardIndexes if any(y in strFullVals for y in x)]
                #If we have a suit, restrict match list
                if len(highCard2) == 2:
                    matchList2 = [x for x in matchList if highCard2[1] in x]
                matchList2 = set(matchList2)
                matchList = set(matchList)
                #If we don't reach this point we only have one set of values, so we know we can return matchList

                #If we reach this point we need to to subtract the values in the smaller set from our larger one
                if len(matchList) > len(matchList2):
                    matchList = matchList.difference(matchList2)
                else:
                    matchList = matchList2.difference(matchList)
                matchList = list(matchList)
            
            rivList += matchList


        # Ts+
        # T+
        elif '+' in subExp:
            #Look up the first value of this (because it must be a rank)
            cardVal = convDict[subExp[:-1]]
            #Get all the values equal to or greater than this value
            fullVals = list(range(cardVal,14))
            #Convert ints back to strs
            strFullVals = [bConvDict[x] for x in fullVals]
            #Get all the cards which match any of these values
            matchList = [x for x in cardIndexes if any(y in strFullVals for y in x)]
            #If we have a suit, restrict match list
            if len(subExp[:-1]) == 2:
                matchList = [x for x in matchList if subExp[1] in x]

            rivList += matchList

        #If no + or -, must be
        # A
        # s
        # As
        else:
            rivList += [x for x in cardIndexes if subExp in x]


        return list((set(rivList)))









def maskConstantsWithVars(cardArray,parMask,fullList,realCards):
    #Just the values we've filtered for with our initial mask
    subArray = cardArray[parMask]

    #print(subArray.shape)

    #iterate over values and apply masks.  Has to be two way.
    #maskD=np.zeros((270725,4),dtype=bool)
    maskTot=np.zeros((len(subArray),4),dtype=bool)
    maskCount=np.zeros((len(subArray)),dtype='int8')

    #We need the total of defined suits, and total of defined ranks
    numRanks = len([x for x in fullList if x[0] != '*'])   #in ['2','3','4','5','6','7','8','9','T','J','Q','K','A','R','O',]])
    numSuits = len([x for x in fullList if x[1] != '?'])   #in ['H','D','C','S']])

    justVals = ['A','K','Q','J','T','9','8','7','6','5','4','3','2','C','S','D','H']
    valVars = ['R','O','N','P','W','X','Y','Z']  #,'?','*']




    countedSuits = np.load(ploDir+'npfiles/00countedSuits.npy')
    countedRanks = np.load(ploDir+'npfiles/00countedRanks.npy')
    countedSuits = countedSuits[parMask]
    countedRanks = countedRanks[parMask]

    #Remove elements from these lists to get what our RONxyz values can be
    remRankC = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    remSuitC = ['H','D','C','S']

    impossRanks = []
    impossSuits = []
    for hc in fullList:
        if hc[0] in remRankC:
            #remRankC.remove(hc[0])
            impossRanks.append(hc[0])
        if hc[1] in remSuitC:
            #remSuitC.remove(hc[1])
            impossSuits.append(hc[1])




    matchedValTally = 0

    for val in fullList:
        #Ad - we have a specific value
        if val[0] in justVals and val[1] in justVals:
            #Get the card we're filtering for
            fVal = realCards.index(val)+1
            #Filter for this value
            maskT = subArray==fVal
            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskT)
            #Total up each row in our mask
            maskC = np.sum(maskT,axis=1)
            maskC = maskC==1
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)

            matchedValTally += 1

        #A? Just rank
        elif val[0] in justVals and val[1] =='?':
            #Count the total number of this rank and have that be the minimum number to filter for
            rankMatch = [x for x in fullList if x[0]==val[0]]
            minCount = len(rankMatch)
            #maxCount = 4 - (len(fullList) - minCount)
            maxCount = 4 - (numRanks - minCount)

            #Get the four rank vals we'll filter for
            rankVals = [realCards.index(x)+1 for x in realCards[:52] if val[0] in x]
            #Apply our mask
            maskT = (subArray==rankVals[0])|(subArray==rankVals[1])|(subArray==rankVals[2])|(subArray==rankVals[3])
            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskT)
            #Total up each row in our mask
            maskC = np.sum(maskT,axis=1)
            maskC = (maskC>=minCount)&(maskC<=maxCount)
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)

            matchedValTally += 1
        
        #*c Just suit
        elif val[1] in justVals and val[0] == '*':
            #Count the total number of this rank and have that be the minimum number to filter for
            suitMatch = [x for x in fullList if x[1]==val[1]]
            minCount = len(suitMatch)
            #maxCount = 4 - (len(fullList) - minCount)
            maxCount = 4 - (numSuits - minCount)
            #print("MIN",minCount,maxCount)

            #Get the four rank vals we'll filter for
            suitVals = [realCards.index(x)+1 for x in realCards[:52] if val[1] in x]
            #Apply our mask
            maskT = (subArray>=min(suitVals))&(subArray<=max(suitVals))  #[1])|(subArray==suitVals[2])|(subArray==suitVals[3])|(subArray==suitVals[4])|(subArray==suitVals[5])|(subArray==suitVals[6])|(subArray==suitVals[7])|(subArray==suitVals[8])|(subArray==suitVals[9])|(subArray==suitVals[10])|(subArray==suitVals[11])|(subArray==suitVals[12])

            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskT)
            #Total up each row in our mask
            maskC = np.sum(maskT,axis=1)
            maskC = (maskC>=minCount)&(maskC<=maxCount)
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)

            matchedValTally += 1

        #Ax Rank and var suit
        elif val[0] in justVals and val[1] in valVars:
            #Count the total number of this rank and have that be the minimum number to filter for
            rankMatch = [x for x in fullList if x[0]==val[0]]
            minCount = len(rankMatch)
            #maxCount = 4 - (len(fullList) - minCount)
            maxCount = 4 - (numRanks - minCount)
            #Get the four rank vals we'll filter for
            rankVals = [realCards.index(x)+1 for x in realCards[:52] if val[0] in x]
            #Apply our mask
            maskT = (subArray==rankVals[0])|(subArray==rankVals[1])|(subArray==rankVals[2])|(subArray==rankVals[3])
            ### Through this point same as previous one, A?, but now we need to filter for suit too

            impossMask = np.zeros_like(subArray,dtype='bool')
            for iv in impossSuits:
                #Get the suit vals we'll filter for
                suitVals = [realCards.index(x)+1 for x in realCards[:52] if iv in x]
                #Apply our mask
                maskS = (subArray>=min(suitVals))&(subArray<=max(suitVals))
                impossMask = np.logical_or(impossMask,maskS)
            #Add min/max suit filter
            suitVMatch = [x for x in fullList if x[1]==val[1]]
            minCountV = len(suitVMatch)
            maxCountV = 4 - (numSuits - minCountV)

            minC = ((minCountV-1)*4)+1
            maxC = ((maxCountV-1)*4)+4
            minMaxMask = (countedSuits >= minC) & (countedSuits <= maxC)
            #Compress these two into one suit filter
            #Need inverse of the impossible cards
            impossMask = np.logical_not(impossMask)
            suitMaskF = np.logical_and(impossMask,minMaxMask)

            #Combine the suit and rank masks
            maskSROverlap = np.logical_and(maskT,suitMaskF)

            ### Now back to same as other one
            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskSROverlap)
            #Total up each row in our mask
            #maskC = np.sum(maskT,axis=1)
            #maskC = (maskC>=minCount)&(maskC<=maxCount)
            #Instead of the above - because we're filtering two ways, only need a match of 1?
            maskRankCheck = np.sum(maskT,axis=1)
            maskRankCheck = (maskRankCheck>=minCount)&(maskRankCheck<=maxCount)
            maskOverlapCheck = np.any(maskSROverlap,axis=1)
            maskC = (maskRankCheck==True) & (maskOverlapCheck==True)

            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)

            matchedValTally += 1


        #Rc - var rank and suit
        elif val[1] in justVals and val[0] in valVars:
            #Count the total number of this rank and have that be the minimum number to filter for
            suitMatch = [x for x in fullList if x[1]==val[1]]
            minCount = len(suitMatch)
            #maxCount = 4 - (len(fullList) - minCount)
            maxCount = 4 - (numSuits - minCount)
            #print("MIN",minCount,maxCount)

            #Get the four rank vals we'll filter for
            suitVals = [realCards.index(x)+1 for x in realCards[:52] if val[1] in x]
            #Apply our mask
            maskT = (subArray>=min(suitVals))&(subArray<=max(suitVals))  #[1])|(subArray==suitVals[2])|(subArray==suitVals[3])|(subArray==suitVals[4])|(subArray==suitVals[5])|(subArray==suitVals[6])|(subArray==suitVals[7])|(subArray==suitVals[8])|(subArray==suitVals[9])|(subArray==suitVals[10])|(subArray==suitVals[11])|(subArray==suitVals[12])

            ### Through this point same as previous one, A?, but now we need to filter for suit too

            impossMask = np.zeros_like(subArray,dtype='bool')
            for iv in impossRanks:
                #Get the suit vals we'll filter for
                rankVals = [realCards.index(x)+1 for x in realCards[:52] if iv in x]
                #Apply our mask
                maskR = (subArray==rankVals[0])|(subArray==rankVals[1])|(subArray==rankVals[2])|(subArray==rankVals[3])

                impossMask = np.logical_or(impossMask,maskR)

            #Add min/max rank filter
            rankVMatch = [x for x in fullList if x[0]==val[0]]
            minCountV = len(rankVMatch)
            maxCountV = 4 - (numRanks - minCountV)
            minC = ((minCountV-1)*13)+1
            maxC = ((maxCountV-1)*13)+13
            minMaxMask = (countedRanks >= minC) & (countedRanks <= maxC)
            #Compress these two into one suit filter
            #Need inverse of the impossible cards
            impossMask = np.logical_not(impossMask)
            rankMaskF = np.logical_and(impossMask,minMaxMask)

            #Combine the suit and rank masks
            maskSROverlap = np.logical_and(maskT,rankMaskF)

            ### Now back to same as other one

            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskSROverlap)
            #Total up each row in our mask
            #maskC = np.sum(maskT,axis=1)
            #maskC = (maskC>=minCount)&(maskC<=maxCount)

            maskSuitCheck = np.sum(maskT,axis=1)
            maskSuitCheck = (maskSuitCheck>=minCount)&(maskSuitCheck<=maxCount)
            maskOverlapCheck = np.any(maskSROverlap,axis=1)
            maskC = (maskSuitCheck==True) & (maskOverlapCheck==True)


            #maskC = np.any(maskT,axis=1)
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)

            matchedValTally += 1


        #Rx - var rank and var suit
        #elif val[0] in valVars and val[1] in valVars:
        else:
            #If our rank is "*", no need to reduce
            if val[0] == '*':
                rankMaskF = np.ones_like(subArray,dtype='bool')
            else:
                #First the rank filters
                impossMaskRank = np.zeros_like(subArray,dtype='bool')
                for iv in impossRanks:
                    #Get the suit vals we'll filter for
                    rankVals = [realCards.index(x)+1 for x in realCards[:52] if iv in x]
                    #Apply our mask
                    maskR = (subArray==rankVals[0])|(subArray==rankVals[1])|(subArray==rankVals[2])|(subArray==rankVals[3])

                    impossMaskRank = np.logical_or(impossMaskRank,maskR)

                #Add min/max rank filter
                rankVMatch = [x for x in fullList if x[0]==val[0]]
                minCountV = len(rankVMatch)
                maxCountV = 4 - (numRanks - minCountV)
                minC = ((minCountV-1)*13)+1
                maxC = ((maxCountV-1)*13)+13

                minMaxMaskR = (countedRanks >= minC) & (countedRanks <= maxC)
                #Compress these two into one suit filter
                #Need inverse of the impossible cards
                impossMaskRank = np.logical_not(impossMaskRank)
                rankMaskF = np.logical_and(impossMaskRank,minMaxMaskR)


            if val[1]=='?':
                suitMaskF = np.ones_like(subArray,dtype='bool')
            else:
                #Now the suit filters
                impossMaskSuits = np.zeros_like(subArray,dtype='bool')
                for iv in impossSuits:
                    #Get the suit vals we'll filter for
                    suitVals = [realCards.index(x)+1 for x in realCards[:52] if iv in x]
                    #Apply our mask
                    maskS = (subArray>=min(suitVals))&(subArray<=max(suitVals))
                    impossMaskSuits = np.logical_or(impossMaskSuits,maskS)
                #Add min/max suit filter
                suitVMatch = [x for x in fullList if x[1]==val[1]]
                minCountV = len(suitVMatch)
                maxCountV = 4 - (numSuits - minCountV)
                minC = ((minCountV-1)*4)+1
                maxC = ((maxCountV-1)*4)+4

                minMaxMaskS = (countedSuits >= minC) & (countedSuits <= maxC)
                #Compress these two into one suit filter
                #Need inverse of the impossible cards
                impossMaskSuits = np.logical_not(impossMaskSuits)
                suitMaskF = np.logical_and(impossMaskSuits,minMaxMaskS)


            #Combine both filters
            combinedMask = np.logical_and(rankMaskF,suitMaskF)

            #Flatten our cumulative mask
            maskTot = np.add(maskTot,combinedMask)
            #Total up each row in our mask
            maskC = np.sum(combinedMask,axis=1)

            maskC = (maskC>=1)  #minCount)&(maskC<=maxCount)
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)





            matchedValTally += 1
        



    #Now we have to do the final tests - sum each row again, make sure it's at least the length of the cardVals fed in
    finalTally = np.sum(maskTot,axis=1)
    #Final is where both the combos at top and the individual hand totals add up to our hand length
    #finalMask = (finalTally>=matchedValTally)&(maskCount>=matchedValTally)
    finalMask = (finalTally>=matchedValTally)&(maskCount>=matchedValTally)
    #print(finalMask.sum())

    #Now we need to apply our finalMask backwards on to the original mask
    #finInverse = np.logical_not(finalMask)

    parMask[parMask] = finalMask

    #parMask[finInverse] = False
    #OR - is above error?
    #finInverse = np.logical_not(finalMask)
    #parMask =

    return parMask


def maskConstants(cardArray,parMask,fullList,realCards):
    #Just the values we've filtered for with our initial mask
    subArray = cardArray[parMask]

    #print(subArray.shape)

    #iterate over values and apply masks.  Has to be two way.
    #maskD=np.zeros((270725,4),dtype=bool)
    maskTot=np.zeros((len(subArray),4),dtype=bool)
    maskCount=np.zeros((len(subArray)),dtype='int8')

    #We need the total of defined suits, and total of defined ranks
    numRanks = len([x for x in fullList if x[0] in ['2','3','4','5','6','7','8','9','T','J','Q','K','A']])
    numSuits = len([x for x in fullList if x[1] in ['H','D','C','S']])

    for val in fullList:
        #Just rank
        if '?' in val:
            #Count the total number of this rank and have that be the minimum number to filter for
            rankMatch = [x for x in fullList if x[0]==val[0]]
            minCount = len(rankMatch)
            #maxCount = 4 - (len(fullList) - minCount)
            maxCount = 4 - (numRanks - minCount)

            #Get the four rank vals we'll filter for
            rankVals = [realCards.index(x)+1 for x in realCards[:52] if val[0] in x]
            #Apply our mask
            maskT = (subArray==rankVals[0])|(subArray==rankVals[1])|(subArray==rankVals[2])|(subArray==rankVals[3])
            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskT)
            #Total up each row in our mask
            maskC = np.sum(maskT,axis=1)
            maskC = (maskC>=minCount)&(maskC<=maxCount)
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)
        
        #Just suit
        elif '*' in val:
            #Count the total number of this rank and have that be the minimum number to filter for
            suitMatch = [x for x in fullList if x[1]==val[1]]
            minCount = len(suitMatch)
            #maxCount = 4 - (len(fullList) - minCount)
            maxCount = 4 - (numSuits - minCount)
            #print("MIN",minCount,maxCount)

            #Get the four rank vals we'll filter for
            suitVals = [realCards.index(x)+1 for x in realCards[:52] if val[1] in x]
            #Apply our mask
            maskT = (subArray>=min(suitVals))&(subArray<=max(suitVals))  #[1])|(subArray==suitVals[2])|(subArray==suitVals[3])|(subArray==suitVals[4])|(subArray==suitVals[5])|(subArray==suitVals[6])|(subArray==suitVals[7])|(subArray==suitVals[8])|(subArray==suitVals[9])|(subArray==suitVals[10])|(subArray==suitVals[11])|(subArray==suitVals[12])

            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskT)
            #Total up each row in our mask
            maskC = np.sum(maskT,axis=1)
            maskC = (maskC>=minCount)&(maskC<=maxCount)
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)

        #Otherwise we have a specific value
        else:
            #Get the four rank vals we'll filter for
            fVal = realCards.index(val)+1
            #Apply our mask
            maskT = subArray==fVal
            #Flatten our cumulative mask
            maskTot = np.add(maskTot,maskT)
            #Total up each row in our mask
            maskC = np.sum(maskT,axis=1)
            maskC = maskC==1
            #Convert this boolean mask to an int mask
            maskC = np.array(maskC,dtype='int8')
            #Add the total count to our cumulative array
            maskCount = np.add(maskCount,maskC)
        

    #Now we have to do the final tests - sum each row again, make sure it's at least the length of the cardVals fed in
    finalTally = np.sum(maskTot,axis=1)
    #Final is where both the combos at top and the individual hand totals add up to our hand length
    finalMask = (finalTally>=len(fullList))&(maskCount>=len(fullList))

    #print(finalMask.sum())

    #Now we need to apply our finalMask backwards on to the original mask
    #finInverse = np.logical_not(finalMask)

    parMask[parMask] = finalMask

    #parMask[finInverse] = False
    #OR - is above error?
    #finInverse = np.logical_not(finalMask)
    #parMask =

    return parMask





def step2VarMatchingConditionA(realCards, subArray, rankValsA, rankValsB, remRankC):

    #Count the total number of this rank and have that be the minimum number to filter for
    #rankValsA = [x for x in realCards[:52] if r1 in x]
    #rankValsB = [x for x in realCards[:52] if r2 in x]
    #Get rid of the ones we can't have
    #rankValsA = [x for x in rankValsA if any(z in x for z in remSuitC)]
    #rankValsB = [x for x in rankValsB if any(z in x for z in remSuitC)]
    # rankValsA = [realCards.index(x)+1 for x in realCards[:52] if r1 in x]
    # rankValsB = [realCards.index(x)+1 for x in realCards[:52] if r2 in x]
    # #Apply our mask
    # maskA = (subArray==rankValsA[0])|(subArray==rankValsA[1])|(subArray==rankValsA[2])|(subArray==rankValsA[3])
    # maskB = (subArray==rankValsB[0])|(subArray==rankValsB[1])|(subArray==rankValsB[2])|(subArray==rankValsB[3])
    # #Get rid of any suits we can't have
    # impossMask = np.zeros_like(subArray,dtype='bool')
    # for iv in impossSuits:
    #     #Get the suit vals we'll filter for
    #     suitVals = [realCards.index(x)+1 for x in realCards[:52] if iv in x]
    #     #Apply our mask
    #     maskS = (subArray>=min(suitVals))&(subArray<=max(suitVals))
    #     impossMask = np.logical_or(impossMask,maskS)
    # #Combine this impossible filter with each ouf our rank masks
    #impossMask = np.logical_not(impossMask)
    #maskA = np.logical_and(impossMask,maskA)
    #maskB = np.logical_and(impossMask,maskB)

    rankValsA = [x for x in realCards[:52] if r1 in x]
    rankValsB = [x for x in realCards[:52] if r2 in x]
    #Get rid of the ones we can't have
    rankValsA = [x for x in rankValsA if any(z in x for z in remSuitC)]
    rankValsB = [x for x in rankValsB if any(z in x for z in remSuitC)]
    rankValsA = [realCards.index(x)+1 for x in rankValsA]
    rankValsB = [realCards.index(x)+1 for x in rankValsB]

    totMask = np.zeros(len(subArray),dtype='bool')
    for li,cardV in enumerate(rankValsA):
        subMask = (subArray==cardV)|(subArray==rankValsB[li])
        subSum = np.sum(subMask,axis=1)
        hit = subSum==2
        totMask = np.logical_or(totMask,hit)


    #Finally add it to our reduce mask
    reduceMask = np.logical_and(reduceMask,totMask)

    return reduceMask

def step2VarMatchingConditionB(realCards, subArray, rankValsA, rankValsB, remRankC):

    rankValsA = [x for x in realCards[:52] if r1 in x]
    rankValsB = [x for x in realCards[:52] if r2 in x]
    #Get rid of the ones we can't have
    rankValsA = [x for x in rankValsA if any(z in x for z in remSuitC)]
    rankValsB = [x for x in rankValsB if any(z in x for z in remSuitC)]
    rankValsA = [realCards.index(x)+1 for x in rankValsA]
    rankValsB = [realCards.index(x)+1 for x in rankValsB]

    #print(rankValsA)

    allMaskedVals = np.zeros_like(subArray,dtype='bool')
    totMask = np.zeros(len(subArray),dtype='bool')
    for li,cardV in enumerate(rankValsA):
        subMask = (subArray==cardV)|(subArray==rankValsB[li])
        allMaskedVals = np.logical_or(allMaskedVals,subMask)

        subSum = np.sum(subMask,axis=1)
        suitedHit = subSum==2
        totMask = np.logical_or(totMask,suitedHit)

    #Our unsuited values are anywhere the allMaskedVals array sum equals 3, OR the totMask is false
    fullArraySum = np.sum(allMaskedVals,axis=1)
    unsuitedThree = fullArraySum>=3

    notSuited = np.logical_not(totMask)

    addMask = np.logical_or(notSuited,unsuitedThree)

    #print("Adding",np.sum(addMask))
    #Finally add it to our reduce mask
    reduceMask = np.logical_and(reduceMask,addMask)

    return reduceMask

def step2VarMatchingConditionC(realCards, subArray, rankValsA, rankValsB, remRankC):


    rankValsA = [x for x in realCards[:52] if s1 in x]
    rankValsB = [x for x in realCards[:52] if s2 in x]
    #Get rid of the ones we can't have
    rankValsA = [x for x in rankValsA if any(z in x for z in remRankC)]
    rankValsB = [x for x in rankValsB if any(z in x for z in remRankC)]
    rankValsA = [realCards.index(x)+1 for x in rankValsA]
    rankValsB = [realCards.index(x)+1 for x in rankValsB]

    totMask = np.zeros(len(subArray),dtype='bool')
    for li,cardV in enumerate(rankValsA):
        subMask = (subArray==cardV)|(subArray==rankValsB[li])
        subSum = np.sum(subMask,axis=1)
        hit = subSum==2
        totMask = np.logical_or(totMask,hit)

    #Finally add it to our reduce mask
    reduceMask = np.logical_and(reduceMask,totMask)

    return reduceMask

def step2VarMatchingConditionD(realCards, subArray, rankValsA, rankValsB, remRankC):



    rankValsA = [x for x in realCards[:52] if s1 in x]
    rankValsB = [x for x in realCards[:52] if s2 in x]
    #Get rid of the ones we can't have
    rankValsA = [x for x in rankValsA if any(z in x for z in remRankC)]
    rankValsB = [x for x in rankValsB if any(z in x for z in remRankC)]
    rankValsA = [realCards.index(x)+1 for x in rankValsA]
    rankValsB = [realCards.index(x)+1 for x in rankValsB]


    allMaskedVals = np.zeros_like(subArray,dtype='bool')
    totMask = np.zeros(len(subArray),dtype='bool')
    for li,cardV in enumerate(rankValsA):
        subMask = (subArray==cardV)|(subArray==rankValsB[li])
        allMaskedVals = np.logical_or(allMaskedVals,subMask)

        subSum = np.sum(subMask,axis=1)
        suitedHit = subSum==2
        totMask = np.logical_or(totMask,suitedHit)

    #Our unsuited values are anywhere the allMaskedVals array sum equals 3, OR the totMask is false
    fullArraySum = np.sum(allMaskedVals,axis=1)
    unsuitedThree = fullArraySum>=3

    notSuited = np.logical_not(totMask)

    addMask = np.logical_or(notSuited,unsuitedThree)

    #Finally add it to our reduce mask
    reduceMask = np.logical_and(reduceMask,addMask)

    return reduceMask

#Go over list, try to filter for each individual pair set to match up all the vars
def step2VarMatching(cardArray,parMask,fullList,realCards):

    #Split cards into individual cards
    #myCards = [fullList[i:i+2] for i in range(0,len(fullList),2)]
    #print("MYCARDS",myCards,"FULLLIST",fullList)
    #Make all possible combos with the cards
    #myCardsCombos = list(itertools.combinations(myCards,2))
    myCardsCombos = list(itertools.combinations(fullList,2))

    rankC = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    rankV = ['R','O','N','P']
    suitC = ['H','D','C','S']
    suitV = ['W','X','Y','Z']

    countedSuits = np.load(ploDir+'npfiles/00countedSuits.npy')
    countedRanks = np.load(ploDir+'npfiles/00countedRanks.npy')
    countedSuits = countedSuits[parMask]
    countedRanks = countedRanks[parMask]
    
    subArray = cardArray[parMask]

    #Remove elements from these lists to get what our RONxyz values can be
    remRankC = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    remSuitC = ['H','D','C','S']
    impossSuits = []
    impossRanks = []
    for hc in fullList:
        if hc[0] in remRankC:
            remRankC.remove(hc[0])
            impossRanks.append(hc[0])
        if hc[1] in remSuitC:
            remSuitC.remove(hc[1])
            impossSuits.append(hc[1])


    reduceMask = np.ones_like(parMask,dtype='bool')
    reduceMask = reduceMask[parMask]

    fullListStr = "".join(fullList)
    mixRank,mixSuit = False,False  #Our values to determine if we need to run the masks
    rankL = [fullListStr[i] for i in range(0,len(fullListStr),2)]
    suitL = [fullListStr[i] for i in range(1,len(fullListStr),2)]
    if any(x in rankC for x in rankL) and any(x in rankV for x in rankL):
        mixRank = True
    if any(x in suitC for x in suitL) and any(x in suitV for x in suitL):
        mixSuit = True

    #print(mixRank,mixSuit,rankL,suitL)
    rankVarSet = set([x for x in rankL if x in rankV])
    rankVarSet = set([x for x in rankVarSet if fullListStr.count(x)>=2])
    suitVarSet = [x for x in suitL if x in suitV]
    suitVarSet = [x for x in suitVarSet if fullListStr.count(x)>=2]
    
    #Iterate over repeated ranks
    #for rv in rankVarSet


    '''
    #First iterate over values looking for one constant and one variable
    for hc in fullList:
        # Ax
        if hc[0] in rankC and hc[1] in suitV:
            if mixRank:
                rankVals = [x for x in realCards[:52] if hc[0] in x]
                rankVals = [x for x in rankVals if x[1] in remSuitC]  #Remove the suits we're saying are impossible
                rankVals = [realCards.index(x)+1 for x in rankVals]
                #Only find one of these rank values
                maskR = np.zeros_like(subArray,dtype='bool')
                #Iterate over possible rank cards individually
                for rv in rankVals:
                    maskT = subArray==rv
                    maskR = np.logical_or(maskR,maskT)

                #Now add a mask for the min/max counts for this var
                minC = fullListStr.count(hc[1])
                minC = ((minC-1)*4)+1
                if minC>=5:  #Only run this if we have xx
                    maskS = (countedSuits>=minC)
                    maskR = np.logical_and(maskR,maskS)

                #Filter for matching rows
                mask = np.any(maskR==True,axis=1)
                mask = np.logical_not(mask)
                reduceMask[mask]=False
        # Rc
        elif hc[1] in suitC and hc[0] in rankV:
            if mixSuit:
                rankVals = [x for x in realCards[:52] if hc[1] in x]
                rankVals = [x for x in rankVals if x[0] in remSuitC]  #Remove the suits we're saying are impossible
                rankVals = [realCards.index(x)+1 for x in rankVals]
                #Only find one of these rank values
                maskR = np.zeros_like(subArray,dtype='bool')
                #Iterate over possible rank cards individually
                for rv in rankVals:
                    maskT = subArray==rv
                    maskR = np.logical_or(maskR,maskT)

                #Now add a mask for the min/max counts for this var
                minC = fullListStr.count(hc[0])
                minC = ((minC-1)*13)+1
                if minC>=14:  #Only run this if we have xx
                    maskS = (countedSuits>=minC)
                    maskR = np.logical_and(maskR,maskS)

                #Filter for matching rows
                mask = np.any(maskR==True,axis=1)
                mask = np.logical_not(mask)
                reduceMask[mask]=False
    '''

    #Now iterate over the list, and where appropriate, check for a match
    for myCombo in myCardsCombos:
        #print("MYCOMBO",myCombo)
        r1 = myCombo[0][0]
        s1 = myCombo[0][1]
        r2 = myCombo[1][0]
        s2 = myCombo[1][1]
        
        #Have handled most of the cases above at this point
        # AxKx, yes
        # AxKy, yes
        # RcRs, yes
        # RcOs, yes
        #Filter for all of the above, and confirm

        # AxKx.
        # Filter for A, filter for K.
        # We can combine these masks, cannot have AxAx.
        # Filter for 5,6,7,8.  Anywhere we match 2 it's a hit.
        if (r1 in rankC and s1 in suitV and r2 in rankC and s2==s1):
            #print(myCombo, "AxKx")

            reduceMask = step2VarMatchingConditionA(realCards, subArray, rankValsA, rankValsB, remRankC)

        # AxKy
        # Filter for A, filter for K.  Separate filters.
        # Want to confirm at least one unique suit value between the two
        # If there are 3, we know it's a hit.
        # If there are two, they just can't be the same suit.
        # So 3=True, 2(AK mask sum) vs 5,6,7,8 - if combined masks = 2, fail, otherwise hit
        elif (r1 in rankC and s1 in suitV and r2 in rankC and s2 in suitV):
            #print(myCombo, "AxKy")
            #print("AxKy",myCombo)

            reduceMask = step2VarMatchingConditionB(realCards, subArray, rankValsA, rankValsB, remRankC)

        # RcRd
        # Same as previous.  Filter for c,d.  Combine the masks, iterate over 55,66,77,88 and
        # look for a hit of 2.
        elif (r1 in rankV and s1 in suitC and r2==r1 and s2 in suitC):
            #print(myCombo, "RcRd")
            reduceMask = step2VarMatchingConditionC(realCards, subArray, rankValsA, rankValsB, remRankC)

        # RcOd
        #
        elif (r1 in rankV and s1 in suitC and r2 in rankV and s2 in suitC):
            #print(myCombo, "RcOd")
            reduceMask = step2VarMatchingConditionD(realCards, subArray, rankValsA, rankValsB, remRankC)


    parMask[parMask] = reduceMask
    return parMask



def rowCheck(rowArray,pattern,bracketVIndexes=None):
    if bracketVIndexes is not None and len(bracketVIndexes)>0:
        bracketDiv2Indexes = [int(x/2) for x in bracketVIndexes]


    #Clean pattern
    rVarList = ["N","O","P","R"]
    rvlI = 0
    sVarList = ["W","X","Y","Z"]
    svlI = 0
    #Make all vars lowercase
    pattern = [x.replace("W","w").replace("X","x").replace("Y","y").replace("Z","z").replace("R","r").replace("O","o").replace("N","n").replace("P","p") for x in pattern]
    #Replace them according to the next val in the varlist
    for pI in range(0,len(pattern)):
        if pattern[pI][0] in ['r','o','n','p']:
            pattern = [x.replace(pattern[pI][0],rVarList[rvlI]) for x in pattern]
            rvlI += 1
        if pattern[pI][1] in ['w','x','y','z']:
            pattern = [x.replace(pattern[pI][1],sVarList[svlI]) for x in pattern]
            svlI += 1


    #Mask where we'll save the checked values
    rcMask = np.zeros(len(rowArray),dtype='bool')
    #See if we need to reduce values below
    patReduce = False
    if len(pattern)!=4:
        patReduce = True
        patVal = len(pattern)

    
    #Convert pattern into one string, then compare everything
    patternStr = "".join(pattern)



    for rowI,row in enumerate(rowArray):
        #Generate all 24 combos of possible line reordering
        combos = list(itertools.permutations(list(row),4))

        #Convert to card values
        #combos = [(cardIndexes[x[0]-1],cardIndexes[x[1]-1],cardIndexes[x[2]-1],cardIndexes[x[3]-1]) for x in combos]
        
        #Cut them down if necessary
        if patReduce:
            combos = [x[:patVal] for x in combos]

        combos = ["".join(x) for x in combos]

        rVarList = ["N","O","P","R"]
        #currRVar = 0
        sVarList = ["W","X","Y","Z"]
        #currSVar = 0
        
        #print("Pattern length",len(pattern),pattern)
        for vI,patV in enumerate(pattern):
            #Rank var handling - first two
            if patV[0] == "*":
                #Get the index value we want to replace
                rvI = 2*vI
                #Then we're saying rank at this spot can be anything, replace it with *
                combos = [x[:rvI]+"*"+x[rvI+1:] for x in combos]

            elif patV[0] in rVarList:
                rvI = 2*vI
                #print("In rVarList",bracketVIndexes,len(bracketVIndexes),vI)
                #return
                #Need to handle the case where we have RRON outside of brackets
                if bracketVIndexes is not None and len(bracketVIndexes)>0 and vI in bracketDiv2Indexes:

                    #rIndexList = [1,3,5]
                    combos = [''.join([x.replace(z[rvI],rVarList[0]) if ind in bracketVIndexes else x for ind,x in enumerate(z)]) for z in combos]
                else:
                    combos = [x.replace(x[rvI],rVarList[0]) for x in combos]
                #Remove the value from our list, going left to right
                rVarList.remove(patV[0])

            if patV[1] == "?":
                svI = (2*vI)+1
                combos = [x[:svI]+"?"+x[svI+1:] for x in combos]

            elif patV[1] in sVarList:
                svI = (2*vI)+1
                combos = [x.replace(x[svI],sVarList[0]) for x in combos]
                sVarList.remove(patV[1])
        

        #print(combos)
        if patternStr in combos:
            rcMask[rowI]=True

    return rcMask
    



'''
import RangeParserFails
import ParserTestDict


testVar = '(80%-20%!RR[AcJc-Ac4c]!JT4!hcd)'  #'cTTsJ'
testVar = '(RR[AcJc-Ac4c])'
j,k=evaluate(testVar)
print("Final combo count",testVar,len(j))

#So theory is - one unattached suit AND one unattached rank (unless it's a pair) and it fails?

asdfi=0
for var in RangeParserFails.failList:
    z,_ = evaluate(var)
    if len(z)!=ParserTestDict.dictSix[var]:
        print("Fail on",var,len(z),ParserTestDict.dictSix[var])
        #break
        asdfi+=1
        if asdfi==100:
            break
    else:
        asdfi+=1
        pass
        #print("Success",var)
'''
#testVar = '**'
#j,k=evaluate(testVar)

#testVar = '(80%-20%!RR[AcJc-Ac4c]!JT4!hcd)'  #'cTTsJ'
#testVar = '(RxOy[6x5x-4x3x])'
#j,k=evaluate(testVar)
#print("Final combo count",testVar,len(j))

#testVar = 'RR[AcJc-Ac7c]'
#j,k=evaluate(testVar)
#print("Final combo count",testVar,len(j))

#testVar = 'RhRd[AA-KK]'
#j,k=evaluate(testVar)
#print("Final combo count",testVar,len(j))
#print(j)

#testVar = 'RxOx[AcJc-Ac7c]'
#j,k=evaluate(testVar)
#print("Final combo count",testVar,len(j))

# testVar = 'AAK'
# j,k=evaluate(testVar)
# print("Final combo count",testVar,len(j))
