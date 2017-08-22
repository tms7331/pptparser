import re

#Pass in a hand range chunk here and confirm it's valid
def confirmHR(exp):
    #At end, compare length of what we've pulled with our regex with length of the exp, they should match
    def checkLength(e1,e2):
        #print("In check length")
        if len(e1) == len(e2):
            #print("same length")
            return True
        else:
            return False

    #Go through different syntax possible, find which category this exp is in and make sure it's valid
    if '$' in exp:
        #macroList = ['$DS','$SS','$NP','$OP','$TP','$NT','$0G','$1G','$2G','$B','$M','$Z','$L','$N','$F','$R','$W']
        macroList = ['$0G','$1G','$2G','$3B10I','$3B10O','$3B12I','$3B12O','$3B15I','$3B15O','$3B2I','$3B2O','$3B4I',
                     '$3B4O','$3B6I','$3B6O','$3B8I','$3B8O','$4B2','$4B3','$4B4','$4B5','$4B6','$FI12','$FI15',
                     '$FI20','$FI25','$FI30','$FI40','$FI50']

        if exp.upper() in macroList:
            return True
        else:
            return False
    
    elif '%' in exp:
        #See if it's a range
        #5%-10% - Hands between the top 5 and top 10 percent of hands (full-ring)
        #1%-100% - All hands
        #5%-10%6h
        
        if '-' in exp:
            verifyExp = re.findall(r'([1-9]\d{0,2}%)(6H)?(-){1}([1-9]\d{0,2}%)(6H)?',exp)
            
            if len(verifyExp) > 0:
                #Verify none of the values are greater than 100
                for pct in verifyExp[0]:
                    if len(pct)==4:
                        if int(pct[:3])>100:
                            return False

                verifyExp = "".join(verifyExp[0])


        #No range, straight percentage
        #15% - The top 15 percent of hands (full-ring)
        #15%6h - The top 15 percent of hands (6-handed)
        else:
            #Want 1-100 %, then optional '6h'
            #verifyExp = re.findall(r'[123456789]\d{0,2}%',exp)
            verifyExp = re.findall(r'([1-9]\d{0,2}%)(6H)?',exp)
            if len(verifyExp) > 0:
                #Verify none of the values are greater than 100
                for pct in verifyExp[0]:

                    if len(pct)==4:
                        if int(pct[:3])>100:
                            return False

                verifyExp = "".join(verifyExp[0])

        return checkLength(verifyExp,exp)


    #Next check for brackets
    elif '[' in exp:
        #Rather than specifically confirm bracket validity (no [K[Q]], etc) just do try/except?
        try:
            bracketList = re.findall(r'\[(.+?)\]',exp)
            cardCount = 0  #Keep track of our total cards used as we iterate through buckets
            #Inside a bracket, we can have -
            #Range of hands (specific like 5s6s-JsQs)
            #Specific hand (J)
            #Specific hands (Js,Ts)
            #RON not allowed
            #wxyz ONLY allowed when they're part of a range (JxTx+)
            #If we have additional info outside of brackets, NO +- allowed, only specific hands
            #Values outside of brackets cannot contain +- ranges, only valid hands
            for bracketSet in bracketList:
                #Can't have RON inside brackets
                if 'R' in bracketSet or 'O' in bracketSet or 'N' in bracketSet or '*' in bracketSet:
                    return False

                #JT+
                #JxTx+
                #Values can be anything, we just need to make sure if one has a suit, they all do
                #suits don't need to match
                elif '+' in bracketSet:
                    #Verify '+' is at the end of the expression, and there's only one +
                    if '+' in bracketSet[:-1]:
                        return False
                    #Make sure it's not the only character
                    if len(bracketSet)==1:
                        return False
                    #Get a list of our cards
                    bracketCards = re.findall('[AKQJT98765432][CSDHWXYZ]?',bracketSet)
                    #Get rid of empty strings
                    bracketCards = [x for x in bracketCards if len(x)>0]
                    #Add this total to our cardCount to verify we don't have too many at the end
                    cardCount += len(bracketCards)
                    #Verify that each element in the list is the same length
                    #if len(set([len(x) for x in bracketCards])) != 1:
                        #return False
                    #Verify that the total length of the elements in the list is equal to the bracket set
                    if len("".join(bracketCards)) != len(bracketSet)-1:
                        return False


                #Same as +, but we need to account for JT-65 type hands, need to be sure both sides match
                elif '-' in bracketSet:
                    #Make sure there's only one -
                    if bracketSet.count('-') != 1:
                        return False
                    #Make sure it's not the only character
                    if len(bracketSet)==1:
                        return False
                    #Split up into before minus, after minus
                    minusSet = re.findall(r'(.*)-(.*)',bracketSet)[0]
                    #[('AKQ', '876')]
                    #[('JT', '')]

                    #Verify our first match is fully valid
                    
                    #Get a list of our cards.  Note that this could return an error, but it's ok with our try/except
                    bracketCards = re.findall('[AKQJT98765432][CSDHWXYZ]?',minusSet[0])
                    #Get rid of empty strings
                    bracketCards = [x for x in bracketCards if len(x)>0]
                    #Add this total to our cardCount to verify we don't have too many at the end
                    cardCount += len(bracketCards)
                    #Verify that each element in the list is the same length
                    #if len(set([len(x) for x in bracketCards])) != 1:
                        #return False
                    #Verify that the total length of the elements in the list is equal to the length of the set
                    if len("".join(bracketCards)) != len(minusSet[0]):
                        return False

                    #Now verify our second match is the equivalent of our first!
                    #This means all suits match, and equivalent rank distance
                    if len(minusSet[1])>0:
                        #Check for equal lengths
                        if len(minusSet[1]) != len(minusSet[0]):
                            return False
                        
                        #Dictionaries to compare rank values
                        convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
                        bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}
                        diffTotals = []
                        #Iterate over cards and check for equivalent values
                        for iCard, card in enumerate(minusSet[0]):
                            #If it's a suit, must be identical
                            #If it's a rank, keep track of distance of first value, make sure all others are the same
                            if card in ['C','S','D','H','W','X','Y','Z']:
                                if minusSet[1][iCard] != card:
                                    return False
                            #If not a suit must be a rank
                            else:
                                diffVal = convDict[card]-convDict[minusSet[1][iCard]]
                                #Don't need to add it if the difference is 0, we support that
                                if diffVal != 0:
                                    diffTotals.append(diffVal)
                        #Now we have a list of the differences between each of the cards
                        #Every difference should be the same, so length of set of this list should be 1
                        if len(set(diffTotals)) != 1:
                            return False


                #If we have multiple values in our bracketSet, confirm each one is valid
                #No wxyz
                #Duplicates ok
                #Split them up by ; and then checking is the same as below for each character
                elif ';' in bracketSet:
                    allVals = bracketSet.split(';')
                    for myCard in allVals:
                        verifyExp = re.findall(r'[AKQJT98765432]?[CSDH]?',myCard)
                        #If it's empty, error
                        if len(verifyExp) == 0:
                            return False
                        #If value of first match doesn't match entire string, error
                        if len(verifyExp[0]) != len(myCard):
                            return False
                    #This can only ever be 1 card
                    cardCount += 1

                #Otherwise we must just have one value
                #Confirm it's valid (no wxyz)
                else:
                    verifyExp = re.findall(r'[AKQJT98765432]?[CSDH]?',bracketSet)
                    #If it's empty, error
                    if len(verifyExp) == 0:
                        return False
                    #If value of first match doesn't match entire string, error
                    if len(verifyExp[0]) != len(bracketSet):
                        return False
                    #This can only ever be 1 card
                    cardCount += 1

                #Remove this bracketSet from our exp, in order to get just the plain characters at the end
                exp = exp.replace('['+bracketSet+']','')


            #Now grab all the values which are NOT inside of brackets, and check those too
            #We already removed all the brackets from exp as we iterated over it, anything left is excess text
            if len(exp)>0:
                #Cannot have a + or - in this, anything else is ok?
                if '+' in exp or '-' in exp:
                    return False
                #Now mostly same as below
                #So this will match one card slot, we can have up to 4 of these
                #verifyExp = re.findall(r'\*|[AKQJT98765432RON]?[CSDHWXYZ]?',exp)
                verifyExp = re.findall(r'[AKQJT98765432RONP\*]?[CSDHWXYZ]?',exp)
                
                #Use list comprehension to get only entries with actual values - regex adds a lot of empty values
                verifyExp = [x for x in verifyExp if len(x)>0]
                
                #Add this total to our cardCount to verify we don't have too many at the end
                cardCount += len(verifyExp)
                
                #Check for repeated characters
                #Get full specific cards
                fullCards = re.findall(r'[AKQJT98765432RONP][CSDHWXYZ]',exp)
                #Now make sure no two of them match
                if len(set(fullCards)) != len(fullCards):
                    return False
                
                #Join together the values
                verifyExp = "".join(verifyExp)
                
                #Return false if we didn't gather all our values outside the brackets
                if not checkLength(verifyExp,exp):
                    return False
                
            #If we've made it through all of the above, need one final check to make sure we've entered maximum of 4 chars
            if cardCount <= 4:
                #If we make it through all these checks and don't return false, statement is valid
                return True

        except:
            return False
        


    elif '+' in exp:
        #Verify '+' is at the end of the expression, and there's only one +
        if '+' in exp[:-1]:
            return False
        #Make sure it's not the only character
        if len(exp)==1:
            return False
        #Get a list of our cards
        bracketCards = re.findall(r'[AKQJT98765432][CSDHWXYZ]?',exp)
        #Get rid of empty strings
        bracketCards = [x for x in bracketCards if len(x)>0]
        if len(bracketCards) > 4:
            return False
        #Verify that each element in the list is the same length
        #if len(set([len(x) for x in bracketCards])) != 1:
            #return False
        #Verify that the total length of the elements in the list is equal to the bracket set
        if len("".join(bracketCards)) != len(exp)-1:
            return False
        return True



    #FIXIT - what if we have a - and a +?
    elif '-' in exp:
        #Make sure there's only one -
        if exp.count('-') != 1:
            return False
        #Make sure it's not the only character
        if len(exp)==1:
            return False
        #Split up into before minus, after minus
        minusSet = re.findall(r'(.*)-(.*)',exp)[0]
        #[('AKQ', '876')]
        #[('JT', '')]

        #Verify our first match is fully valid
        
        #Get a list of our cards.  Note that this could return an error, but it's ok with our try/except
        bracketCards = re.findall('[AKQJT98765432][CSDHWXYZ]?',minusSet[0])
        #Get rid of empty strings

        bracketCards = [x for x in bracketCards if len(x)>0]
        #Make sure we don't have too many cards
        if len(bracketCards) > 4:
            return False
        #Verify that each element in the list is the same length  - don't need this!  [T8c-53c] is valid
        #if len(set([len(x) for x in bracketCards])) != 1:
            #return False
        #Verify that the total length of the elements in the list is equal to the length of the set
        if len("".join(bracketCards)) != len(minusSet[0]):
            return False

        #Now verify our second match is the equivalent of our first!
        #This means all suits match, and equivalent rank distance
        if len(minusSet[1])>0:
            #Check for equal lengths
            if len(minusSet[1]) != len(minusSet[0]):
                return False
            
            #Dictionaries to compare rank values
            convDict = {'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}
            bConvDict = {13:'A',12:'K',11:'Q',10:'J',9:'T',8:'9',7:'8',6:'7',5:'6',4:'5',3:'4',2:'3',1:'2'}
            diffTotals = []
            #Iterate over cards and check for equivalent values
            for iCard, card in enumerate(minusSet[0]):
                #If it's a suit, must be identical
                #If it's a rank, keep track of distance of first value, make sure all others are the same
                if card in ['C','S','D','H','W','X','Y','Z']:
                    if minusSet[1][iCard] != card:
                        return False
                #If not a suit must be a rank
                else:
                    diffVal = convDict[card]-convDict[minusSet[1][iCard]]
                    if diffVal != 0:                
                        diffTotals.append(diffVal)
            #Now we have a list of the differences between each of the cards
            #Every difference should be the same, so length of set of this list should be 1
            if len(set(diffTotals)) != 1:
                return False

        #If we haven't hit an error so far, must be valid!
        return True




    #Last case - no ranges, brackets, etc, just raw text
    else:
        #print("FOUND ELSE CASE")

        #So this will match one card slot, we can have up to 4 of these
        #verifyExp = re.findall(r'\*|[AKQJT98765432RON]?[CSDHWXYZ]?',exp)
        verifyExp = re.findall(r'[AKQJT98765432RONP\*]?[CSDHWXYZ]?',exp)
        #print(verifyExp)
        #Use list comprehension to get only entries with actual values - regex adds a lot of empty values
        verifyExp = [x for x in verifyExp if len(x)>0]
        #print(verifyExp)
        #See if it's empty or too long.  Should have between 1 and 4 values.
        if len(verifyExp)==0 or len(verifyExp)>4:
            return False

        #Check for repeated characters
        #Get full specific cards
        fullCards = re.findall(r'[AKQJT98765432RONP][CSDHWXYZ]',exp)
        #Now make sure no two of them match
        if len(set(fullCards)) != len(fullCards):
            return False

        #Join together the values
        verifyExp = "".join(verifyExp)

        #print(verifyExp)
        #print(exp)

        
        return checkLength(verifyExp,exp)
        


    


def chunkExpression(exp):
    retExp = re.findall(r'\(|\)|,|!|\:|[^\(\),!\:]*',exp)
    return retExp[:-1]  #The -1 because there's always an empty list element at the end for some reason

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
    myExp = myExp.replace('$0G', 'AKQJ-')
    myExp = myExp.replace('$1G', '(AKQT-,AKJT-,AQJT-)')
    myExp = myExp.replace('$2G', '(AKQ9-,AKT9-,AJT9-)')
    myExp = myExp.replace('$B', '[A-J]')
    myExp = myExp.replace('$M', '[T-7]')
    myExp = myExp.replace('$Z', '[6-2]')
    myExp = myExp.replace('$L', '[A,2,3,4,5,6,7,8]')
    myExp = myExp.replace('$N', '[K-9]')
    myExp = myExp.replace('$F', '[K-J]')
    myExp = myExp.replace('$R', '[A-T]')
    myExp = myExp.replace('$W', '[A,2,3,4,5]')
    
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




def confirmExpression(exp):
    ##Iterate over expression, if it's not (),!: it's an expression we need to parse

    #Must make everything upper case, and convert all ',' inside of brackets into ';'
    exp = exp.upper()
    
    '''Don't need this now - doing it in cleanExpression()
    #Find commas in between brackets, replace with ;
    bracketList = re.findall(r'\[.+?\]',exp)
    if bracketList:
        for bracketSet in bracketList:
            #if there's a comma inside of this bracket set
            if ',' in bracketSet:
                #Replace the comma with ; in a temp var
                replaceVar = bracketSet.replace(',',';')
                exp = exp.replace(bracketSet, replaceVar)
    '''

    #Chunk expression so we can iterate over it
    exp = cleanExpression(exp)
    exp = chunkExpression(exp)


    #Count opening/closing parenthesis
    pCount = 0
    for char in exp:
        if char == '(':
            pCount +=1
        elif char == ')':
            pCount -= 1
        if pCount < 0:
            return False
    if pCount != 0:
        return False

    #print("Line 346, past parenthesis count")

    #Look at rest of range, make sure char ordering is valid
    for i in range(len(exp)):
        c=exp[i]
        if i+1 < len(exp):
            n=exp[i+1]
        else:
            n='END'

        #All chars ( ) , : ! exp END

        #Valid: ( or exp
        #Invalid ) , : ! END
        if c == '(':
            if n==')' or n==',' or n==':' or n=='!' or n=='END':
                return False

        #Valid: ) , : ! END
        #Invalid ( exp
        elif c == ')':
            if n!=')' and n!=',' and n!=':' and n!='!' and n!='END':
                return False

        #Valid ( exp
        #Invalid all else
        elif c == ',':
            #Make sure it's not the first character
            if i==0:
                return False
            if n== ')' or n== ',' or n== ':' or n== '!' or n== 'END':
                return False

        #Valid ( exp
        #Invalid ) , : ! END
        elif c == ':':
            #Make sure it's not the first character
            if i==0:
                return False
            if n==')' or n==',' or n==':' or n=='!' or n=='END':
                return False
        #Same as above
        elif c == '!':
            #Make sure it's not the first character
            if i==0:
                return False
            if n==')' or n==',' or n==':' or n=='!' or n=='END':
                return False

        #Otherwise we have an expression, evaluate it and make sure it's valid
        #Valid ) , : ! END
        #Invalid ( exp
        else:
            if n!=')' and n!=',' and n!=':' and n!='!' and n!='END':
                return False
            #print("Confirming HR!")
            valid = confirmHR(c)
            if not valid:
                return False

    #If we've iterated over everything and haven't hit an error, it must be valid
    return True




####################### CHECK RIVER EXP SYNTAX ########################

#Confirms a river expression is syntactically valid
# A
# s
# As
# A-5
# As-5s
# Ts-
# Ts+
def validateRiverExp(exp):
    #Separate by commas, then comfirm each part matches one of the above patterns
    exp = exp.upper()
    exp = exp.split(",")
    
    try:
        for subExp in exp:
            #If it's an empty string - meaning we have two commas, or a comma at beginning or end
            if subExp == '':
                return False

            if '-' in subExp:
                #Make sure only one match
                if subExp.count('-')>1 or '+' in subExp:
                    return False

                #Split string
                subExpSplit = subExp.split("-")  #Returns a list of 2 elements, second can be empty string

                #Make sure first string isn't empty
                if len(subExpSplit[0]) == 0:
                    return False

                #Check both sides have the same suit if there is a suit, and consist of valid characters
                myMatch = re.findall(r'[AKQJT98765432][CSDH]?',subExpSplit[0])
                myMatch2 = re.findall(r'[AKQJT98765432][CSDH]?',subExpSplit[1])

                # print(myMatch,myMatch2)
                # print(len("".join(myMatch)),len(myMatch),len("".join(myMatch2)),(len(myMatch2)))
                #Make sure length of eqch one equals the length of their expression
                #if len("".join(myMatch)) != len(myMatch[0]):
                    #return False
                
                #Verify we only matched one card.  T, or Ts
                if len(myMatch) > 1:
                    return False
                ### FIXIT ### - do we need to have this be "".join(myMatch) for the length stuff?  taking length of list here?
                #If we have a second one, verify that if we have a suit, it's the same suit
                if len(myMatch2) > 0:
                    if len("".join(myMatch2)) != len(myMatch2[0]):
                        return False
                    #Make sure they're the same length
                    if len(myMatch[0]) != len(myMatch2[0]):
                        return False
                    #Check for a suit
                    if len(myMatch[0])==2:
                        if myMatch[0][1] != myMatch2[0][1]:
                            return False

                    #Make sure sum of each side adds up to all the non - chars
                    if len(myMatch[0])+len(myMatch2[0]) != len(subExp)-1:
                        return False
                #If we only have one expression, make sure ita dds up to the length of exp
                else:
                    if len(myMatch[0]) != len(subExp)-1:
                        return False




            elif '+' in subExp:
                #Make sure we just have one plus, at the end of the string
                if '+' in subExp[:-1] or '-' in subExp:
                    return False

                myMatch = re.findall(r'[AKQJT98765432][CSDH]?',subExp)
                
                #Verify that the total length of the elements in the list is equal to the bracket set
                #if len("".join(myMatch)) != len(myMatch[0]):
                if len(myMatch[0]) != len(subExp)-1:
                    return False
                
                #Verify we only matched one card.  T, or Ts
                if len(myMatch) > 1:
                    return False



            else:
                #Match A s As format
                myMatch = re.findall(r'[AKQJT98765432]?[CSDH]?',subExp)
                #Make sure we matched something
                
                if len(myMatch) > 0:
                    if len(myMatch[0]) != len(subExp):
                        return False

                else:
                    return False

        #If we didn't hit any falses, must be valid!
        return True
    except:
        return False



def confirmBoard(board):
    board=board.upper()
    myMatch = re.findall(r'[AKQJT98765432][CSDH]',board)

    matchedStr = "".join(myMatch)
    if len(matchedStr)==len(board):
        return True
    else:
        return False

