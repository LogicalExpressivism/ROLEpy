import copy
import os
from datetime import datetime

connectives = ['and', 'or', 'implies', 'not'] #The list of connectives
sides = ['antecedent', 'consequent']
paths = ['Atoms', 'Runs']
Forest = {} #Vestigial forest, I'm going to try to eliminate this
now = datetime.now() #Date and time of program start
dt_string = now.strftime('%d-%m-%Y-%H-%M-%S.txt') #date and time as a filename to be used later
CO = True #Whether we accept reflexive sequents

for path in paths: #first thing we do is make a new file for this run in each of Atomic and Runs
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, dt_string), 'a') as temp_file:
        temp_file.write('Root; Location; Antecedent; Consequent; Atomic; Reflexive')

def debrak(string):
    if string != ' ':
        string = ''.join(string)
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace('\n', '')
        string = string.replace('\\', '')
        string = string.replace('\'', '')
        string = string.split(',')
    return string

class Sequent:
    def __init__(self, root, location, antecedent, consequent, atomic, reflexive):
        self.root = root #the name we want to call the sequent by, just some string for ease of memory; I'm not married to having fancy names, but it certainly makes debugging easier
        self.location = location #A string of characters that when followed in the right way lead us uniquely to a sequent in the forest. L = Left, R = Right, M = Middle. Roots are always M.
        self.antecedent = antecedent #A list of strings, which are the antecedents
        self.consequent = consequent #A list of strings, which are the consequentskillers = Sequent('killers', 'M', '(Socrates is human implies Socrates is mortal),((Socrates is human or Socrates is dancer) and (not (Socrates is dancer)))', '(Socrates is mortal)', False, False)
        self.atomic = atomic #Whether the sequent is atomic
        self.reflexive = reflexive #whether the sequent is reflexive or an instance of CO

    def deparen(self): #removes outermost parentheses
        for side in sides: #runs once per side of the turnstile
            if getattr(self, side) != ' ': #This doesn't work if the antecedent or consequent is empty, obviously
                sentences = getattr(self, side) #holds onto the sentences 
                setattr(self, side, []) #clears the sentences
                propset = []
                for sentence in sentences: #for each premise or conclusion in the antecedent or consequent:
                    print(sentence)
                    if (len(sentence) == 0): continue
                    letters = list(sentence)
                    if letters[0] == '(' and letters[-1] == ')': #Only runs if the first and last character are '(' and ')'
                        valid = True #i.e., it is valid to remove the outermost parentheses
                        count = 0 #times we have encountered an unpaired '('
                        iterations = 0 #index of the currently investigated character
                        for letter in letters:                      #To make sure we only remove the outermost parentheses, we assume we can and test the result if we did
                            if valid == True:                       #Each open or clase paren modifies the count and we should end with a count of 0; each '(' has a ')'
                                iterations = iterations + 1         #If before the end we get a count below 0, we must have a paren without a partner
                                if letter == '(':                   #Therefore the outermost parentheses are not connected
                                    count = count + 1               #Therefore we shouldn't remove the outermost parentheses
                                if letter == ')':                   #
                                    count = count - 1               #
                                if count <= 0:                      #
                                    if iterations < len(letters):   #
                                        valid = False               #
                        if valid == True: #If the sequent is still valid after the test, we need to delete the outermost parentheses
                            del letters[0] 
                            del letters[-1]
                            newsentence = ''.join(letters) #Put the characters back together
                            propset.append(newsentence)
                        elif valid == False:
                            propset.append(sentence)
                    else:
                        propset.append(sentence)
                setattr(self, side, propset)

    def atomcheck(self):    #determines whether a sequent is atomic
        self.deparen()
        atomic = True       #assume first that it is atomic
        for side in sides:
            for x in getattr(self, side):   #for each side of the turnstile
                if atomic == True:
                    for y in connectives:       #we check for each connective
                        if y in x.split(' '):   #if the connective is present
                            atomic = False      #the sequent was not atomic
        self.atomic = atomic

    def refcheck(self):     #determines whether a sequent is reflexive
        self.deparen()
        reflexive = False   #assume first that it is not
        for x in self.antecedent:       #for each antecedent
            for y in self.consequent:   #and each consequent
                if x == y:              #if the two match
                    reflexive = True    #we have reflexivity
        self.reflexive = reflexive

    def mainsave(self, printseq):   #does most of the work for storing information toreduce repetition in the code
        if self.atomic == True:     #if the sequent is atomic, we use each file
            for path in paths:      #'Atoms' and 'Runs'
                with open(os.path.join(path, dt_string), 'a') as temp_file: #opens the relevant file
                    temp_file.write(printseq)                               #writes the current sequent to it
        else:
            with open(os.path.join('Runs', dt_string), 'a') as temp_file:   #if the sequent is not atomic
                temp_file.write(printseq)                                   #we only print to 'Runs'
        
    def printout(self):
        self.deparen()       #remove outer parentheses
        for side in sides:
            for prop in getattr(self, side):
                if len(prop) > 0:
                    prop = list(prop)
                    if prop[0] == ' ':
                        del prop[0]
                    prop = ''.join(prop)    
        self.atomcheck()    #updates atomicity
        self.refcheck()     #updates reflexivity
        printseq = str('\n' + str(self.root) + ';' + str(self.location) + ';' + str(self.antecedent) + ';' + str(self.consequent) + ';' + str(self.atomic) + ';' + str(self.reflexive)) #This is the format I've settled on
        if CO == True:      #if we allow reflexivity to be saved 
            self.mainsave(printseq) #everything is simple                       
        else:
            if self.reflexive == False: #if the sequent is not reflexive
                self.mainsave(printseq) #we save it
            else:                       #otherwise
                fileread = open(os.path.join('Runs', dt_string), 'r')   #we open 'Runs'
                lines = fileread.readlines()                            #get the lines in the file
                fileread.close()                                        #close the file
                lastline = lines[-1]                                    #check the last line
                if lastline != '\n[Proof search terminated due to reflexive sequent]':  #If the last line doesn't tell us the search has stopped
                    with open(os.path.join('Runs', dt_string), 'a') as temp_file:       #we open the file
                        temp_file.write('\n[Proof search terminated due to reflexive sequent]')     #and let the user know the search has stopped
                        ##Of course the search hasn't really stopped, we've just stopped updating the file when we continue to decompose sequents.
                        ##It's just easier this way and doesn't really impact runtime
                
    def spcleanup(self):  #cleans up rule applications for single-parent rules
        self.location = str(self.location + 'M') #alters the sequents location
        self.printout() #saves the sequent to file

    def tpcleanup(self, side, position, lpar, rpar):    #cleans up rule applications for two-parent rules
        lpar.location = str(lpar.location + 'L')        #Updates locations for saving
        rpar.location = str(rpar.location + 'R')        #Updates locations for saving
        for x in (lpar, rpar):                          #for each of our new sequents
            del getattr(x, side)[position]              #deletes the main proposition
            x.atomcheck()                               #updates sequents' atomicity
            x.printout()                                #saves both parents
        if lpar.atomic == False:                        #if the left parent is not atomic, we want to decompose it next
            self.location = lpar.location               #we set the working sequent's location accordingly
            for x in sides:                             #
                setattr(self, x, getattr(lpar, x))      #and we update the working sequent's antecedent and consequent
        else:                                           #if it is, then we decompose the right parent
            self.location = rpar.location               #set the location
            for x in sides:                             #
                setattr(self, x, getattr(rpar, x))      #set the antecedent and consequent
        
    def rulework(self, side, position, index): #does the repetitive heavy lifting for rule decomposition
        mainprop = getattr(self, side)              #gets the relevant side of the sequent
        mainprop = mainprop[position].split(' ')    #gets just the proposition on which we operate
        before = ' '.join(mainprop[:index])         #gets everything before the connective
        after = ' '.join(mainprop[index + 1:])      #gets everything after the connective
        result = [before, after]                    #puts these in an easy-to-handle format
        return result                               #returns the result

    def notrule(self, side, position, index): #applies negation rules
        if side == 'antecedent': 
            self.consequent.append(self.rulework(side, position, index)[1])        #puts the negatum sans operator into the conclusions
            del self.antecedent[position]          #deletes the negation from the antecedent 
        elif side == 'consequent':
            self.antecedent.append(self.rulework(side, position, index)[1])           #puts the negatum sans operator into the premises
            del self.consequent[position]       #deletes the negation from the consequent
        self.spcleanup()                        #cleans up

    def ifrule(self, side, position, index): #applies conditional rules
        if side == 'antecedent':                                            #applies left conditional
            lpar = copy.deepcopy(self)                                      #makes a copy of the sequent to turn into the left parent
            rpar = copy.deepcopy(self)                                      #makes a copy of the sequent to turn into the right parent
            for x in sides:
                for y in [lpar, rpar]:
                    setattr(y, x, list(getattr(y, x)))
            lpar.consequent.append(self.rulework(side, position, index)[0]) #alters the consequent accordingly
            rpar.antecedent.append(self.rulework(side, position, index)[1]) #alters the antecedent accordingly
            self.tpcleanup(side, position, lpar, rpar)                      #cleans up and saves
        elif side == 'consequent':                                          #applies right conditional
            self.antecedent.append(self.rulework(side, position, index)[0]) #
            self.consequent.append(self.rulework(side, position, index)[1])
            del self.consequent[position]
            self.spcleanup()               

    def spmult(self, side, position, index): #Rule applications for single parent multiplicative rules (L&, RV)  
        for x in (0, 1):  #for each of rulework's results
            getattr(self, side).append(self.rulework(side, position, index)[x])
        del getattr(self, side)[position]               #removes the decomposed proposition from the sequent
        self.spcleanup()                                #cleans up

    def tpadd(self, side, position, index): #Rule applications for two-parent additive rules (LV, R&)
        lpar = copy.deepcopy(self)                                          #make a copy of this sequent to turn into the left parent
        rpar = copy.deepcopy(self)                                          #make a copy of the sequent to turn into the right parent
        for x in sides:
            for y in [lpar, rpar]:
                setattr(y, x, list(getattr(y, x)))
        getattr(lpar, side).append(self.rulework(side, position, index)[0]) #alter the antecedent/consequent accordingly 
        getattr(rpar, side).append(self.rulework(side, position, index)[1]) #alter the antecedent/consequent accordingly
        self.tpcleanup(side, position, lpar, rpar)                          #cleans up
        
    def router(self, connective, side, position, index):
        if (connective == 'and' and side == 'antecedent') or (connective == 'or' and side == 'consequent'):
            self.spmult(side, position, index)
        if (connective == 'and' and side == 'consequent') or (connective == 'or' and side == 'antecedent'):
            self.tpadd(side, position, index)
        if connective == 'implies':
            self.ifrule(side, position, index)
        if connective == 'not':
            self.notrule(side, position, index)

    def parser(self):
        self.atomcheck()
        if self.atomic == False:
            found = False
            index = []
            connective = []
            side = []
            position = []
            for x in sides:
                if found == False:
                    position = -1
                    for propositions in getattr(self, x):
                        if found == False:
                            position = position + 1
                            degree = 0
                            num = -1
                            for word in propositions.split(' '):
                                if found == False:
                                    num = num + 1
                                    if word in connectives:
                                        if degree == 0:
                                            index = num
                                            connective = word
                                            side = x
                                            found = True
                                    else:
                                        for letter in list (word):
                                            if letter == '(':
                                                degree = degree + 1
                                            elif letter == ')':
                                                degree = degree - 1
            if found == True:
                self.router(connective, side, position, index)
            elif found == False:
                for y in self.location:
                    if y == 'L':
                        print ('There are no more complex sentences to decompose, and really you shouldn\'t even be able to see this message.')
                        quit()
                        
    def main(self):
        self.atomcheck()
        while self.atomic == False:
            self.parser()
        for x in range (0, len(self.location) - 1):
            backstr = self.location[::-1]
            if backstr[x] == 'L':
                newloc = backstr.replace('L', 'R', 1)[::-1]
                if x != 0:
                    newloc = newloc[:-x]
                self.location = newloc
                fileread = open(os.path.join('Runs', dt_string), 'r')
                got = False
                for line in fileread:
                    if got == False:
                        if self.root == line.split(';')[0]:
                            if newloc == line.split(';')[1]:
                                got = True
                                self.antecedent = debrak(line.split(';')[2])
                                self.consequent = debrak(line.split(';')[3])
                fileread.close()
                self.main()
            
def init():
    if os.path.exists('Sequents.txt'): #Checks whether there is such a file locally
        f = open('Sequents.txt', 'r') #opens it if there is
    else:
        f = open('Sequents.txt', 'x') #creates one if not
    for line in f:
        line = line.replace('\n', '')
        line = line.replace('\'', '')
        seq = line.split(';')
        for x in (2, 3):
            if seq[x] == '':
                seq[x] = ' '
        Seq = Sequent(seq[0], seq[1], debrak(seq[2]), debrak(seq[3]), seq[4], seq[5])
        Seq.printout()
        Seq.main()

##    
    
