import itertools
import re
import numpy as np
import os

# try:
#     from . import SyntaxValidator as sv
# except:
#     import SyntaxValidator as sv

import SyntaxValidator as sv

PLODIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLODIR = PLODIR + '/PPTParser/'
RANKEDHUARRAY = np.load(PLODIR+'npfiles/pptRankedHUnums.npy')

ARR = np.load(PLODIR+'npfiles/pptSeparateRankSuit.npy')


ALLRANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
ALLRANKVARS = ['R','O','N','P']

ALLSUITS = ['H','D','C','S']
ALLSUITVARS = ['W','X','Y','Z']

CARDINDEXES = ['2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AH',
               '2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AD',
               '2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AC',
               '2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS','AS']


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

        return expandRange(char,self.filterArray)


#Take in a range and an optional startMask
def expandRange(rangeStr, startMask=None):
    #preloadedArrays = ['*']  #,'**','***','****','XXYY','XXYZ','RR','RRON']
    macroList = ['$0G','$1G','$2G','$3B10I','$3B10O','$3B12I','$3B12O','$3B15I','$3B15O','$3B2I','$3B2O','$3B4I',
                 '$3B4O','$3B6I','$3B6O','$3B8I','$3B8O','$4B2','$4B3','$4B4','$4B5','$4B6','$FI12','$FI15',
                 '$FI20','$FI25','$FI30','$FI40','$FI50']
    if rangeStr in macroList:
        retSet = loadMask(rangeStr, startMask)
        return retSet

    #Handle pct - if we have this it's the only value we can have
    if '%' in rangeStr:
        retSet = pctHandler(rangeStr, startMask)
        #FIXIT - need to account for 5%-10%
        #myR = set(fullList[:pct])
        #return myR
        return retSet

    else:
        #Need to match the pattern

        #Goal is to clean hand a bit.  Can chunk together connected parts
        groupedList = re.findall(r'\[(.+?)\]',rangeStr)

        #Remove all the info in brackets from rangeString
        for bracketSet in groupedList:
            rangeStr = rangeStr.replace('['+bracketSet+']','')

        #And now we can append whatever is left outside of the brackets to this list
        groupedList.append(rangeStr)

        handTuples = []
        ####### Now go through each of our chunks and clean it
        for g in groupedList:
            #We'll have replaced commas with semicolons in a previous cleaning step

            #for PLUS, return ('plus',5h6s)
            #for MINUS, return ('minus',7?7?)
            #For RANGE, return ('range',[4?,T?])
            if ";" in g:
                ret = commaHandler(g)
                handTuples.append((1,"comma",ret))
            elif '+' in g:
                ret = plusHandler(g)
                leng = len(ret)/2
                handTuples.append((leng,"plus",ret))
            elif '-' in g:
                minusOrRange, ret = minusHandler(g)
                if minusOrRange=="minus":
                    leng=len(ret)/2
                else:
                    #print(minusOrRange,ret)
                    leng=len(ret[0])/2
                handTuples.append((leng,minusOrRange,ret))
            #Otherwise plain hand
            else:
                ret = cleanString(g)
                leng = len(ret)/2
                handTuples.append((leng,"plain",ret))


        #Now we'll have the lists in some format
        cardDict = {"rank":[],"suit":[],"rankDependency":[],"suitDependency":[],"commaSeparated":[]}
        numVars = int(sum([x[0] for x in handTuples]))
        #print("NUMVAJRS",numVars,type(numVars))

        cardDictList = [cardDict.copy() for _ in range(numVars)]

        suitCards = []
        #First take care of our suits
        currIndex=0
        for h in handTuples:
            for i in range(int(h[0])):
                if h[1]=="comma":
                    suitCards.append((currIndex,"#"))
                elif h[1]=="range":
                    suit = h[2][0][i*2+1]
                    suitCards.append((currIndex,suit))
                else:
                    suit = h[2][i*2+1]
                    suitCards.append((currIndex,suit))
                currIndex+=1

        #Go through and assign suits to our cardDicts
        #suitCards = [(0,"C"),(1,"X"),(2,"X")]
        cardDictList = suitHandling(cardDictList,suitCards)

        #The RONP values do NOT apply to anything in parenthesis, only +-
        #Can handle each chunk separately
        hIndex = 0
        for h in handTuples:
            if h[1]=="comma":
                cardDictList = rankHandlingComma(cardDictList,hIndex,h)
            elif h[1]=="plus" or h[1]=="minus":
                cardDictList = rankHandlingPlusMinus(cardDictList,hIndex,h)
            elif h[1]=="range":
                cardDictList = rankHandlingRange(cardDictList,hIndex,h)
            elif h[1]=="plain":
                cardDictList = rankHandlingPlain(cardDictList,hIndex,h)
                
            #Need to increment our index by number of cards we just covered
            hIndex+=h[0]

        #Take our cardDicts and create a numpy mask
        finalMatchStr = matchCardDicts(cardDictList)
        finalMask = createArray(finalMatchStr,numVars)

        if startMask is not None:
            finalMask = np.logical_and(finalMask,startMask)

        return finalMask


def matchCardDicts(cardList):
    '''
    cardList is list of constraints for each card
    [{'rank': [(13, '==')], 'suit': [(2, '==')], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}, {'rank': [(13, '==')], 'suit': [(3, '==')], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}, {'rank': [(13, '!=')], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}]
    '''

    finalMatchStr = []
    for cIndex,c in enumerate(cardList):
        #8 total columns, pairs of ranks/suits for hands
        rankIndex = cIndex*2
        suitIndex = cIndex*2+1

        #Ranks will be lists of tuples, in rankVal/operator order
        #(7,==)
        #(8,<=)
        #And for specific ranges we can have TWO and combine them, <=8 and >=4
        if c["rank"]:
            rankStr = ["(ARR[:,COL{}]{}{})".format(rankIndex,x[1],x[0]) for x in c["rank"]]
            rankStr = " & ".join(rankStr)
            finalMatchStr.append(rankStr)
        #Same as rank, list of tuples of (suit,relation)
        if c["suit"]:
            suitStr = ["(ARR[:,COL{}]{}{})".format(suitIndex,x[1],x[0]) for x in c["suit"]]
            suitStr = " & ".join(suitStr)
            finalMatchStr.append(suitStr)
        #Rank dependency:
        #(0,==,+1)  Index, relation, optional +- value
        #(1,!=,"")
        if c["rankDependency"]:
            rankDependStr = ["(ARR[:,COL{}]{}ARR[:,COL{}]{})".format(rankIndex,x[1],x[0]*2,x[2]) for x in c["rankDependency"]]
            rankDependStr = " & ".join(rankDependStr)
            finalMatchStr.append(rankDependStr)
        #Suit dependency:
        #Will just be equal or !=
        #(1, !=)
        if c["suitDependency"]:
            suitDependStr = ["(ARR[:,COL{}]{}ARR[:,COL{}])".format(suitIndex,x[1],x[0]*2+1) for x in c["suitDependency"]]
            suitDependStr = " & ".join(suitDependStr)
            finalMatchStr.append(suitDependStr)
        #Comma separated list of conditions, only works for concrete hands?  No +-
        #This need to be joined grouped together separately with |
        #(A,d),(K,c),(8,"")
        if c["commaSeparated"]:
            commaDependStr = []
            for tup in c["commaSeparated"]:
                #print("TUP",tup)
                if tup[0] and tup[1]:
                    currStr = "(ARR[:,COL{}]=={}) & (ARR[:,COL{}]=={})".format(rankIndex,tup[0],suitIndex,tup[1])
                elif tup[0]:
                    currStr = "(ARR[:,COL{}]=={})".format(rankIndex,tup[0])
                elif tup[1]:
                    currStr = "(ARR[:,COL{}]=={})".format(suitIndex,tup[1])
                commaDependStr.append(currStr)
            commaDependStr = " | ".join(commaDependStr)
            commaDependStr = "("+commaDependStr+")"
            finalMatchStr.append(commaDependStr)

    finalMatchStr = " & ".join(finalMatchStr)

    #If there are no conditions (Such as when hand is 'RW') return plain string
    if finalMatchStr:
        finalMatchStr = "(" + finalMatchStr + ")"
    
    #print(finalMatchStr)
    return finalMatchStr


def createArray(finalMatchStr,cardListLeng):
    '''
    finalMatchStr is match condition, but with COLNUM indicating relative column indexes
    ((ARR[:,COL0]==13) & (ARR[:,COL1]==2) & (ARR[:,COL2]==13) & (ARR[:,COL3]==3) & (ARR[:,COL4]!=13))
    
    cardListLeng is how many different cards we've specified
    '''

    #If there are no conditions (Such as when hand is 'RW') return mask of all true
    if not finalMatchStr:
        mask = np.ones(270725,dtype='bool')
        return mask
    
    #Assign our real card indexes over their temporary COL vals
    indexes=[(0,1),(2,3),(4,5),(6,7)]
    replaceList = itertools.permutations(indexes,cardListLeng)
    #Example with cardListLeng 2 -
    #[((0, 1), (2, 3)), ((0, 1), (4, 5)), ((0, 1), (6, 7)), ((2, 3), (0, 1)), ((2, 3), 
    #(4, 5)), ((2, 3), (6, 7)), ((4, 5), (0, 1)), ((4, 5), (2, 3)), ((4, 5), (6, 7)), 
    #((6, 7), (0, 1)), ((6, 7), (2, 3)), ((6, 7), (4, 5))]

    conditions = []
    for replaceIndexTuple in replaceList:
        #(1,2)
        newStr = finalMatchStr  #Create a copy of our str to overwrite
        for ind in range(cardListLeng):
            rankInd = ind*2
            suitInd = ind*2+1

            newStr = newStr.replace("COL"+str(rankInd),str(replaceIndexTuple[ind][0])).replace("COL"+str(suitInd),str(replaceIndexTuple[ind][1]))

        conditions.append(newStr)

    #Each individual condition combined
    finalSearch = " | ".join(conditions)
    #((ARR[:,0]==13) & (ARR[:,1]==2) & (ARR[:,2]==13) & (ARR[:,3]==3) & (ARR[:,4]!=13)) 
    # | ((ARR[:,0]==13) & (ARR[:,1]==2) & (ARR[:,2]==13) & (ARR[:,3]==3) & (ARR[:,6]!=13))...

    #Impossible to get here without crashing with anything malicious, so don't worry about check?
    mask = eval(finalSearch)

    return mask



def rankHandlingComma(cardDictList,hIndex,h):
    '''
    cardDictList is the dict we want to write our info to
    [{'rank': [], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}]
    
    hIndex is current index in cardDictList we're writing to

    h is info about these values
    (1, 'comma', ['A?', 'K?', 'Q?'])
    '''

    numValues = h[0]
    #hDesc = h[1]  #comma, plus, minus, range, plain
    hValues = h[2]  #LISTS if comma or range, otherwise a string

    allCommaList = []

    #We will have a LIST of len(2) strings
    for card in hValues:
        #print("CARD",card)
        rank = card[0]
        suit = card[1]

        el1 = ""
        el2 = ""

        if rank in ALLRANKS:
            el1=ALLRANKS.index(rank)+1
        if suit in ALLSUITS:
            el2=ALLSUITS.index(suit)+1
        tup = (el1,el2)

        allCommaList.append(tup)

    cardDictList[int(hIndex)]["commaSeparated"]=allCommaList

    return cardDictList

def rankHandlingPlusMinus(cardDictList,hIndex,h):
    '''
    cardDictList is the dict we want to write our info to
    [{'rank': [], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}]
    
    hIndex is current index in cardDictList we're writing to

    h is info about these values
    (1.0, 'plus', 'J?')
    '''

    #h is a TUPLE
    numValues = h[0]
    hDesc = h[1]  #comma, plus, minus, range, plain
    hValues = h[2]  #LISTS if comma or range, otherwise a string

    if hDesc=="plus":
        relativeSymbol = ">="
    else:
        relativeSymbol = "<="

    #Will be a string in format of 5c6c

    #Already handled suits, only need ranks
    #Establish our baseline rank
    baselineRank = ALLRANKS.index(hValues[0])+1
    baselineIndex = int(hIndex)
    cardDictList[baselineIndex]["rank"]=[(baselineRank,relativeSymbol)]

    #Set the others in relation to this card
    for i in range(2,len(hValues),2):

        rank = ALLRANKS.index(hValues[i])+1
        relative = rank - baselineRank

        if relative==0:
            relativeStr = ""
        elif relative>0:
            relativeStr="+{}".format(relative)
        else:
            relativeStr = str(relative)

        #Need to increment our index
        hIndex += 1

        cardDictList[int(hIndex)]["rankDependency"] = cardDictList[int(hIndex)]["rankDependency"] + [(baselineIndex,"==",relativeStr)]

    return cardDictList

def rankHandlingRange(cardDictList,hIndex,h):
    '''
    cardDictList is the dict we want to write our info to
    [{'rank': [], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}]
    
    hIndex is current index in cardDictList we're writing to

    h is info about these values
    (1.0, 'range', ['J?', '8?'])
    '''

    #h is a TUPLE
    numValues = h[0]
    #hDesc = h[1]  #comma, plus, minus, range, plain
    hValues = h[2]  #LISTS if comma or range, otherwise a string

    #Since we've already handled the ranks we have to be sure we retain the order

    #Let's build lists of (index,rank) for identical ranks and different ranks
    sameRankTuples = []
    changeRankTuples = []
    for i in range(0,len(hValues[0]),2):
        if hValues[0][i]==hValues[1][i]:
            sameRankTuples.append((int(i/2),hValues[0][i]))
        else:
            changeRankTuples.append((int(i/2),hValues[0][i],hValues[1][i]))

    #Assign specific values for sameRank cards
    for rankTup in sameRankTuples:
        cardIndex = int(rankTup[0] + hIndex)
        cardRank = rankTup[1]
        cardDictList[cardIndex]["rank"]=[(ALLRANKS.index(cardRank)+1,"==")]

    #Establish the range for our baseline card that covers a range
    baselineRank = changeRankTuples[0][1]
    baselineRank2 = changeRankTuples[0][2]

    #Convert to integers
    baselineRank = ALLRANKS.index(baselineRank)+1
    baselineRank2 = ALLRANKS.index(baselineRank2)+1

    if baselineRank>baselineRank2:
        geOrder = ("<=",">=")
    else:
        geOrder = (">=","<=")

    #Convert to our real card index
    baselineCardIndex = int(changeRankTuples[0][0] + hIndex)
    cardDictList[baselineCardIndex]["rank"]=[(baselineRank,geOrder[0]),(baselineRank2,geOrder[1])]


    #Set the others relative to this index
    for rankTup in changeRankTuples[1:]:
        cardIndex = int(rankTup[0] + hIndex)
        cardRank = ALLRANKS.index(rankTup[1])+1

        relative = cardRank - baselineRank
        if relative==0:
            relativeStr = ""
        elif relative>0:
            relativeStr="+{}".format(relative)
        else:
            relativeStr = str(relative)

        cardDictList[cardIndex]["rankDependency"] = cardDictList[cardIndex]["rankDependency"] + [(baselineCardIndex,"==",relativeStr)]

    return cardDictList



def rankHandlingPlain(cardDictList,hIndex,h):
    '''
    cardDictList is the dict we want to write our info to
    [{'rank': [], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}]
    
    hIndex is current index in cardDictList we're writing to

    h is info about these values
    (1.0, 'plain', 'JC')
    '''

    #hIndex is the index of the first card being passed here
    #h is the list of cards in tuple form, second is the type

    #h is a TUPLE
    numValues = h[0]
    hValues = h[2]

    #This will be a STRING, AcKh or R?R?K
    #Handling should be similar to suits, match up the vars

    seenRanks = []
    seenRankVars = []

    #cardDictList = [{'rank': [], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}, {'rank': [], 'suit': [], 'rankDependency': [], 'suitDependency': [], 'commaSeparated': []}]

    #cardDict = {"rank":[1],"suit":None,"rankDependency":None,"suitDependency":None,"commaSeparated":None}
    #        numVars = int(sum([x[0] for x in handTuples]))
    #cardDictList = [cardDict.copy() for _ in range(2)]
    #cardDictList = [{"rank":[1],"suit":None,"rankDependency":None,"suitDependency":None,"commaSeparated":None},{"rank":[1],"suit":None,"rankDependency":None,"suitDependency":None,"commaSeparated":None}]

    rankVarTup = []
    for i in range(0,len(hValues),2):
        rankVarTup.append((int(i/2),hValues[i]))
    #print("RVT INDEXES",rankVarTup)
    for rankTup in rankVarTup:

        rankIndex = int(rankTup[0] + hIndex)
        rank = rankTup[1]

        #print("RANK INDEJX",rankIndex,rankTup[0],hIndex)

        #Set this index equal to this card
        if rank in ALLRANKS:
            #cardDictList[rankIndex]["rank"] = 3
            #print("CURRENT ASSIGNMENT",cardDictList[rankIndex])
            #print("CURRENT ASSIGNMENTB",cardDictList)

            cardDictList[rankIndex]["rank"]=[(ALLRANKS.index(rank)+1,"==")]
            #print("ASSIGNING RANK INDEX< VAL",rankIndex, rank)
            #Need to set indexes of all vars NOT EQUAL to this card
            #print("CURR",cardDictList)
            #cardDictList[0]["rank"]=[(123,456)]
            #print("CURR2",cardDictList)
            #raise Exception
            if rank not in seenRanks:
                seenVars = []
                for rankTup2 in rankVarTup:
                    if rankTup2[1] in ALLRANKVARS and rankTup2[1] not in seenVars:
                        #print("OVERWRITING")
                        tup2Index = int(rankTup2[0] + hIndex)
                        cardDictList[tup2Index]["rank"]=cardDictList[tup2Index]["rank"]+[(ALLRANKS.index(rank)+1,"!=")]

                        seenVars.append(rankTup2[1])

                #Add our rank to the list of ranks we've already done as we don't need to set comparisons twice
                seenRanks.append(rank)


        #Set it equal to any identical var, unequal to any different var
        elif rank in ALLRANKVARS and rank not in seenRankVars:
            #print("CONDITION 2?")
            subSeenRankVar = []
            for rankTup2 in rankVarTup:

                newVar = rankTup2[1]
                newIndex = int(rankTup2[0]+hIndex)

                if newVar in ALLRANKVARS and newVar not in seenRankVars and newVar not in subSeenRankVar:
                    #print("NEW VAR,RANK",newVar,rank)
                    #print("NEW INDEX,RANKINDEX",newIndex,rankIndex)
                    if newVar==rank and newIndex!=rankIndex:
                        relation="=="
                        #cardDictList[newIndex]["rankDependency"].append((rankIndex,relation,""))
                        cardDictList[newIndex]["rankDependency"]=cardDictList[newIndex]["rankDependency"]+[(rankIndex,relation,"")]

                        #subSeenRankVar.append(newVar)

                    elif newVar!=rank:
                        relation="!="

                        #cardDictList[newIndex]["rankDependency"].append((rankIndex,relation,""))
                        cardDictList[newIndex]["rankDependency"]=cardDictList[newIndex]["rankDependency"]+[(rankIndex,relation,"")]

                        subSeenRankVar.append(newVar)

            seenRankVars.append(rank)



    return cardDictList




def suitHandling(cardDictList,suitCards):
    #suitCards = [(0,"C"),(1,"X"),(2,"X")]

    #print("SUITCADS",suitCards)
    #Possible suit vars are:
    # CDSH WXYZ ? #

    #List to keep track of which suits have already been matched up
    seenSuits = []

    #And 
    for suitTupIndex,suitTup in enumerate(suitCards):
        suitTupIndex = suitTup[0]
        suitTupCard = suitTup[1]

        #If it's in CDSH, set index==suitValue
        #Set one of each var to != suitValue
        if suitTupCard in ALLSUITS:
            #Same as rank, list of tuples of (suit,relation)
            cardDictList[suitTupIndex]["suit"]=[(ALLSUITS.index(suitTupCard)+1,"==")]

            #Only need to set the vars!= if we haven't seen this suit yet
            if suitTupCard not in seenSuits:
                suitVars = [x for x in suitCards if x[1] in ALLSUITVARS]

                seenSuitVars = []
                for suitVarTup in suitVars:
                    if suitVarTup[1] not in seenSuitVars:
                        #For each different varaible, set one of them to != this suit
                        cardDictList[suitVarTup[0]]["suit"]=cardDictList[suitVarTup[0]]["suit"]+[(ALLSUITS.index(suitTupCard)+1,"!=")]
                        seenSuitVars.append(suitVarTup[1])

                seenSuits.append(suitTupCard)

        #If it's in WXYZ, only need to look at other vars, set == index and !=index as needed
        elif suitTupCard in ALLSUITVARS and suitTupCard not in seenSuits:
            #(1, !=)

            #suitvars = [x for x in suitCards[:suitTupIndex] if x[1] in ALLSUITVARS+["#"]]
            seenSuitVars = []
            for suitVarTup in suitCards:
                #print("COMARISON",suitVarTup[1],"OURS",suitTupCard)
                #Only need to handle once for each var
                if suitVarTup[1] in seenSuitVars or suitVarTup[1] in seenSuits:
                    #print("IN SEENSUITS",seenSuitVars,seenSuits)
                    continue
                #Our card
                if suitVarTup[1]==suitTupCard:
                    #print("SAME",suitVarTup,suitTupCard,suitTupIndex)
                    #Make sure it's a different index - pointless to set it identical to self
                    if suitVarTup[0]==suitTupIndex:
                        #print("SAME INDEX")
                        #print("BREAKING")
                        continue
                    #print("EQUAL")
                    cardDictList[suitVarTup[0]]["suitDependency"] = cardDictList[suitVarTup[0]]["suitDependency"]+[(suitTupIndex,"==")]
                    #seenSuitVars.append(suitTupCard)

                # Going to handle these separately now
                # #A comma separated suit card
                # elif suitVarTup[1]=="#":
                #     cardDictList[suitVarTup[0]]["suitDependency"] = cardDictList[suitVarTup[0]]["suitDependency"] +[(suitTupIndex,"!=")]
                #     #cardDictList[suitTupIndex]["suitDependency"].append((suitVarTup[0],"!="))

                #A different var
                elif suitVarTup[1] in ALLSUITVARS:
                    #print("CASE3")
                    #print("ADDING !=",cardDictList)
                    #cardDictList[suitVarTup[0]]["suitDependency"].append((suitTupIndex,"!="))
                    cardDictList[suitVarTup[0]]["suitDependency"] = cardDictList[suitVarTup[0]]["suitDependency"] + [(suitTupIndex,"!=")]
                    #print("ADDED !=",cardDictList)
                    #cardDictList[suitTupIndex]["suitDependency"].append((suitVarTup[0],"!="))
                    #print("APPENDING TO SEENSUITVARS",)
                    seenSuitVars.append(suitVarTup[1])


            #print("ROUND SUITVAR",cardDictList)
            seenSuits.append(suitTupCard)

            # equalIndexes = [(x[0],"==") for x in suitCards[:suitTupIndex] if x[1]==suitTupCard]

            # unequalIndexes = [(x[0],"!=") for x in suitCards[:suitTupIndex] if (x[1] in ALLSUITVARS+["#"] and x[1]!=suitTupCard)]


            # unequalRanks = [currVarDict["suits"][x] for x in currVarDict["suits"] if x!=suit]
            # unequal = [(x,"!=") for x in unequalRanks]

            # cardDictList[suitTupIndex]["suitDependency"]=equalIndexes+unequalIndexes


        #Case of comma separated, set all previous vars to != this INDEX
        elif suitTupCard=="#":

            suitvars = [x for x in suitCards if x[1] in ALLSUITVARS]
            #print("SUIT VARS",suitvars)
            seenSuitVars = []
            for suitVarTup in suitvars:
                if suitVarTup[1] not in seenSuitVars:
                    cardDictList[suitVarTup[0]]["suitDependency"]=cardDictList[suitVarTup[0]]["suitDependency"]+[(suitTupIndex,"!=")]

                    seenSuitVars.append(suitVarTup[1])


    return cardDictList



def commaHandler(bString):
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




def cleanString(st):
    '''
    Input is a string, 1-8 characters, any combination of suits and ranks.
    Output is length 8 string with all missing suits/ranks filled in with * and ?
    '''

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
    #convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
    #bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}

    #First we need to clean the data, either confirm suits are there or add suits
    pString = pString[:pString.find('+')]
    pString = cleanString(pString)

    return pString



def minusHandler(mString):
    '''
    Input is some string containing a -, such as 55-, 7s8s-
    Output is an enumerated list of the matches for this range, such as 55, 44, 33, etc

    Will only be a single string with a single -, multiple would be separated in different brackets
    '''
    #Decrease each card in the list by 1 until we have a value equal to A
    convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
    bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}
    
    #First we need to clean the data, either confirm suits are there or add suits
    mString = mString.split("-")  #Returns a LIST!
    #print("MSTRING",mString)

    #Get our basic string for the starting range
    mStringA = cleanString(mString[0])

    #print("MSTRINGA",mStringA)
    if not mString[1]:
        return "minus",mStringA

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

    #Want to return a list of only first and last
    retListF = [retList[0],retList[-1]]

    return "range",retListF





def evaluate(expression,board=None,rangeFilter=None):
    #Confirm it's a valid expression
    #print("EVAL!")
    if sv.confirmExpression(expression):
        #Clean and chunk expression
        expression = sv.cleanExpression(expression)
        expression = sv.chunkExpression(expression)
        #print("EXPRESSION",expression)
        #If we have a board, create a numpy mask using this board
        if board is not None:
            rangeFilter = makeBoardMask(board)
        
        p = ExpressionParser(expression,rangeFilter)

        handList = p.getValue()

        #cardArray = getCardArray()
        #Want to return both the array and the mask
        return RANKEDHUARRAY[handList], handList
    else:
        raise Exception("Invalid Hand")



def makeBoardMask(board):
    '''
    Input is a board string, in format '2H5HTDJC'
    Output is a mask representing the values in our basic hand array that are
    blocked by the cards on this board
    '''
    #cardArray = getCardArray()

    board=board.upper()

    #boardVals = [board[i:i+2] for i in range(0, len(board), 2)]
    cardIndexes = ['2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AH',
                   '2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AD',
                   '2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AC',
                   '2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS','AS']

    #[x[i:i+2] for i in range(0, len(x), 2)]  #Splice by 2
    #cardIndexes.index(x)+1  #Just get indexes
    boardVals = [cardIndexes.index(board[i:i+2])+1 for i in range(0, len(board), 2)]

    #FIXIT - can clean up this mask
    boardMask=np.zeros((270725,4),dtype=bool)
    for bv in boardVals:

        boardM = RANKEDHUARRAY == bv
        boardMask = np.add(boardMask,boardM)

    maskTally = np.sum(boardMask,axis=1)

    retMask = maskTally == 0

    return retMask



############################################
###########################################

def pctHandler(r, startMask):
    '''
    Inputs: r is a string of a percentage
    Four cases - 3%, 3%6h, 30%-50%, 30%-50%6h

    startMask is an optional parameter of hands that are known to be impossible

    Returns array with the hands represented by this string
    '''
    
    pctMask = np.zeros(270725,dtype='bool')

    if '6H' in r:
        #parMask = np.load(PLODIR+'/npfiles/'+myPattern+'.npy')
        orderedList = np.load(PLODIR+'npfiles/pptRanked6maxMap.npy')
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

    myMask = np.load(PLODIR+'npfiles/'+myMacro+'.npy')

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











testVar = "Jc"
j,k=evaluate(testVar)
print(len(j))

#testVar = "3%-10%:sJdTh,s4s4h4:RcRs[Tx9x-4x3x]"
#j,k=evaluate(testVar)
#print(len(j))

#ERROR HANDS, [2c,3c,4c,5c,6c]xxx - WILL include AcKcQc2c.  [2c-6c]xxx will NOT include that hand
#Failure point - [AA-]rr will include 2222, [22-]rr will NOT include quad 2s


#Test basic xx, xy, rr, rn
#Run through all examples



#Fix all of our matching function to convert indexes to proper values
#Redo our suits function so it doesnt double match, only need ONE match here


#Run a few more tests, then cleanup and put on Github
