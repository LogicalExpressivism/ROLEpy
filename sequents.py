## Instructions:
 ## Sequent.planter() takes a sequent and makes it an entry in Forest 
## Sequent.deparen() removes outermost parentheses for parsing, which allows us to use as many parentheses we want when specifying connectives
## Sequent.parser() takes a sequent and finds out where and what the main connective is of the leftmost logically complex sentence and sends that info to router()
## Sequent.router() shuffles that sequent off to the appropriate decomposition algorithm
## each decomposition algorithm takes the leftmost logically complex sentence (of the correct type, along with important info from parser()) and attaches one or more trees to the entry in the Forest of the same name, keeping track of heredity 
## Sequent.gamut() takes a previously specified sequent, plants it, and runs the parser
## debug() prints the whole forest in a mostly easy to read way (for now, until the forest gets too big) to check whether everything is as it should be
##
## main() is the main operator. It takes a sequent, plants it if it isn't already planted, and decomposes it to atoms.
##
## Sequents must be formatted thus: Sequent('SOME_STRING', 'M', ['(FIRST_PREMISE)', '(SECOND_PREMISEa) CONNECTIVE (SECOND_PREMISEb)'], ['(CONCLUSION)'])
## Each root sequent should begin with a location of 'M' and each sentence should be separated from connectives and each other by parentheses. 
## For example, my sequent 'killers', a reference to Human by The Killers, is:
## Sequent('killers', 'M', ['(Socrates is human implies Socrates is mortal)', '((Socrates is human or Socrates is dancer) and (not (Socrates is dancer)))'], ['(Socrates is mortal)'])
##
## A note about how decomposition works:
## Currently, the main function can only keep one version of the sequent it's working on in memory at a time. This means we can't go back once the function starts running. In the decomposition functions,
## you will see us create a sequent, add it to the forest, and then change the parameters of that same sequent. Because of the way this works (that is, because I couldn't figure out how to do this in a
## better way) the sequents in the forest and the sequent on which the decomposition functions operate are different objects. If there is a way to load sequents from the forest and work on those directly,
## that might be preferable in the long run, since it might allow us to hop around the tree with the right sort of navigation function.
##
#############################################


import copy
import os


Connectives = ["and", "or", "implies", "not"]
Forest = {} #Dictionary containing the Trees

class Sequent: #AKA the Trees
   def __init__(self, name, location, antecedent, consequent):
      self.name = name #the name we want to call the sequent by, just some string for ease of memory; I'm not married to having fancy names, but it certainly makes debugging easier
      self.location = location #A string of characters that when followed in the right way lead us uniquely to a sequent in the forest. L = Left, R = Right, M = Middle. Roots are always M.
      self.antecedent = antecedent #A list of strings, which are the antecedents
      self.consequent = consequent #A list of strings, which are the consequents

   def planter(self): #Takes a sequent from wherever we can get it and plants it as a tree in the forest or updates the tree if it already exists in the forest
                      #Each Tree is a dictionary of locations, which are each dictionaries of antecedents and consequents
      if str(self.name) not in Forest:
         Forest[self.name] = {}
      Forest[self.name][self.location] = {}
      Forest[self.name][self.location]['Antecedents'] = copy.deepcopy(self.antecedent)
      Forest[self.name][self.location]['Consequents'] = copy.deepcopy(self.consequent)

   def atomcheck(self):
      atomic = True
      for x in self.antecedent:
         for y in Connectives:
            if y in x.split(' '):
               atomic = False
      for x in self.consequent:
         for y in Connectives:
            if y in x.split(' '):
               atomic = False
      return atomic

   def deparen(self):                        #For each proposition in the sequent, removes the
      ##outermost parentheses (()).
##      self.primer()
      if self.antecedent != [""]:            #It causes problems if we pass an empty set into this
         premises = self.antecedent               #holds onto antecedent
         self.antecedent = []                   #clears antecedent for overwriting
         for premise in premises:                       
            letters = list(premise) #splits the proposition into characters
            if letters[0] == "(" and letters[-1] == ")":    #checks whether the outermost characters are in fact parentheses
               valid = True                     #Whether we want to remove outer brackets
               count = 0                        #number of open parens
               iterations = 0                   #times we've checked whether a character is a paren
               for letter in letters:
                  if valid == True:                #To make sure we want to remove the outermost parentheses, we first assume we do and have the code show we don't. 
                     iterations = iterations + 1   #Each open or close parentheses modifies the count and after we've counted up everything, we should end up at 0; each open paren has a partner.
                     if letter == "(":             #If at any point before the end of the line the count comes below zero, we must have been mistaken and not every open paren has a partner.
                        count = count + 1          #In that case the outermost parentheses are not connected to each other and should not be removed lest we end up in a "A) or (B" situation, which would be bad
                     if letter == ")":             #In that case, we revise whether we want to remove the parentheses and skip along to the next premise
                        count = count - 1
                     if count <= 0:             
                        if iterations < len(letters):
                           valid = False
               if valid == True:
                  del letters[0]
                  del letters[-1]
                  newpremise = "".join(letters)                   #Puts the proposition back into sentence form
                  self.antecedent.append(newpremise)        #repopulates the antecedent
                  valid = False
               elif valid == False:
                  self.antecedent.append(premise)
            else:
               self.antecedent.append(premise)
      if self.consequent != [""]:            #It causes problems if we pass an empty set into
         ##this
         conclusions = self.consequent               #holds onto antecedent
         self.consequent = []                   #clears antecedent for overwriting
         for conclusion in conclusions:                       
            letters = list(conclusion) #splits the proposition into characters
            if letters[0] == "(" and letters[-1] == ")":    #checks whether the outermost characters are in fact parentheses
               valid = True                     #Whether we want to remove outer brackets
               count = 0                        #number of open parens
               iterations = 0                   #times we've checked whether this character is a paren
               for letter in letters:
                  if valid == True:
                     iterations = iterations + 1  
                     if letter == "(":                  
                        count = count + 1
                     if letter == ")":
                        count = count - 1
                     if count <= 0:             #If we ever hit 0 before the very last close
                        ##character in the sentence, we know something's wrong --- they're
                        ##mismatched
                        if iterations < len(letters):
                           valid = False
               if valid == True:
                  del letters[0]
                  del letters[-1]
                  newconclusion = "".join(letters)                   #Puts the proposition back into sentence
                  ##form
                  self.consequent.append(newconclusion)        #repopulates the antecedent
                  valid = False
               elif valid == False:
                  self.consequent.append(conclusion)
            else:
               self.consequent.append(conclusion)
      self.planter()

   def land(self, position, index): #Position is the place of the sentence in the antecedent we're decomposing (starting at 0); index is the place in that sentence of the word which is the main connective
      location = str(self.location + 'M') #marks and alters the location of the sequent for later
      premises = copy.deepcopy(self.antecedent) #makes a copy of the premises on which we can operate
      mainprop = premises[position].split(" ") #separates the relevant premise into a list of its words
      del premises[position] #deletes the sentence on which we operate from the premise, we'll put it back together later
      ahead = " ".join(mainprop[0:index]) #puts together all the words before the connecive, i.e., the first conjunct
      behind = " ".join(mainprop[index + 1:]) #puts together all the words after the connective, i.e., the second conjunct
      premises.append(ahead) #puts the first conjunct back into the antecedent
      premises.append(behind) #puts the second conjunct back into the antecedent
      levelup = Sequent(self.name, location, premises, self.consequent) #the sequent we started with but with a new antecedent
      levelup.planter() #adds the sequent to the Forest
      self.location = location #applies the change in location to the new sequent to the sequent we're currently working on
      self.antecedent = premises #applies the change in premises to the new sequent to the sequent we're currently working on
        
   def lor(self, position, index):
      lpremises = copy.deepcopy(self.antecedent) #premises to be used in the left parent
      lconclusions = copy.deepcopy(self.consequent) #conclusions to be used in the left parent
      rpremises = copy.deepcopy(self.antecedent) #premises to be used in the right parent
      rconclusions = copy.deepcopy(self.consequent) #conclusions to be used in the right parent
      mainprop = rpremises[position].split(" ") #splits the sentence containing the main connective into words––rpremises and lpremises are interchangeable here
      del lpremises[position] #removes the disjunction from the premises
      del rpremises[position] #removes the disjunction from the premises
      ahead = " ".join(mainprop[0:index]) #puts the left disjunct back together
      behind = " ".join(mainprop[index + 1:]) #puts the right disjunct back together
      rpremises.append(behind) #puts one disjunct in the premises of the right parent
      lpremises.append(ahead) #puts the other disjunct in the premises of the left parent
      llocation = str(self.location + 'L') #changes the location for the left parent
      llevelup = Sequent(self.name, llocation, lpremises, lconclusions) #creates a placeholder sequent for the left parent
      llevelup.planter() #plants the left parent
      rlocation = str(self.location + 'R') #changes the location for the right parent
      rlevelup = Sequent(self.name, rlocation, rpremises, rconclusions) #creates a placeholder sequent for the right parent
      rlevelup.planter() #plants the right parent
      if self.atomcheck() == False:       #If the resulting left parent is not atomic, we want to operate on it next
         self.location = llocation
         self.antecedent = lpremises
         self.consequent = lconclusions   #If the resulting left parent is atomic, we want to operate on the right parent instead.
      elif self.atomcheck() == True:
         self.location = rlocation
         self.antecedent = rpremises
         self.consequent = rconclusions
   
   def lif(self, position, index):
      lpremises = copy.deepcopy(self.antecedent) #premises to be used in the left parent
      lconclusions = copy.deepcopy(self.consequent) #conclusions to be used in the left parent
      rpremises = copy.deepcopy(self.antecedent) #premises to be used in the right parent
      rconclusions = copy.deepcopy(self.consequent) #conclusions to be used in the right parent
      mainprop = rpremises[position].split(" ") #splits the sentence containing the main connective into words––rpremises and lpremises are interchangeable here
      del lpremises[position] #removes the conditional from the premises 
      del rpremises[position] #removes the conditional from the premises
      ahead = " ".join(mainprop[0:index]) #puts the antecedent back together
      behind = " ".join(mainprop[index + 1:]) #puts the consequent back together
      rpremises.append(behind) #puts the antecedent into the premises of the right parent
      lconclusions.append(ahead) #puts the consequent into the conclusions of the left parent
      llocation = str(self.location + 'L') #changes the location for the left parent
      llevelup = Sequent(self.name, llocation, lpremises, lconclusions) #creates a placeholder sequent for the left parent
      llevelup.planter() #plants the left parent
      rlocation = str(self.location + 'R') #changes the location for the right parent
      rlevelup = Sequent(self.name, rlocation, rpremises, rconclusions) #creates a placeholder sequent for the right parent
      rlevelup.planter() #plants the right parent
      if self.atomcheck() == False: #if the resulting left parent is not atomic, we want to operate on it next
         self.location = llocation
         self.antecedent = lpremises
         self.consequent = lconclusions
      elif self.atomcheck() == True: #if the resulting left parent is atomic, we want to operate on the right parent instead
         self.location = rlocation
         self.antecedent = rpremises
         self.consequent = rconclusions
         
   def lneg(self, position, index): 
      location = str(self.location + 'M') #marks and alters the location of the sequent for later
      premises = copy.deepcopy(self.antecedent) #copies the premises
      conclusions = copy.deepcopy(self.consequent) #copies the conclusions
      mainprop = premises[position].split(" ") #splits the sentence containing the main connective into words
      del premises[position] #removes the negatum from the sequent
      del mainprop[index] #removes the negation from the negatum
      prop = " ".join(mainprop) #puts the negatum back together
      conclusions.append(prop) #puts the negatum (sans negation) in the conclusions
      levelup = Sequent(self.name, location, premises, conclusions) #creates a placeholder sequent
      levelup.planter() #plants the parent
      self.location = location #alters the sequent 
      self.consequent = conclusions #alters the sequent 
      self.antecedent = premises #alters the sequent
         
   def rand(self, position, index): #See notes for lor; they are the same except l and r are swapped in the natural places
      lpremises = copy.deepcopy(self.antecedent)
      lconclusions = copy.deepcopy(self.consequent)
      rpremises = copy.deepcopy(self.antecedent)
      rconclusions = copy.deepcopy(self.consequent)
      mainprop = rconclusions[position].split(" ")
      del lconclusions[position]
      del rconclusions[position]
      ahead = " ".join(mainprop[0:index])
      behind = " ".join(mainprop[index + 1:])
      rconclusions.append(behind)
      lconclusions.append(ahead)
      llocation = str(self.location + 'L')
      llevelup = Sequent(self.name, llocation, lpremises, lconclusions)
      llevelup.planter()
      rlocation = str(self.location + 'R')
      rlevelup = Sequent(self.name, rlocation, rpremises, rconclusions)
      rlevelup.planter()
      if self.atomcheck() == False:
         self.location = llocation
         self.antecedent = lpremises
         self.consequent = lconclusions
      elif self.atomcheck() == True:
         self.location = rlocation
         self.antecedent = rpremises
         self.consequent = rconclusions
         
   def ror(self, position, index): #See notes for land; they are the same except l and r are swapped in the natural places
      location = str(self.location + 'M')
      conclusions = copy.deepcopy(self.consequent)
      mainprop = conclusions[position].split(" ")
      del conclusions[position]
      ahead = " ".join(mainprop[0:index])
      behind = " ".join(mainprop[index + 1:])
      conclusions.append(ahead)
      conclusions.append(behind)
      levelup = Sequent(self.name, location, self.antecedent, conclusions)
      levelup.planter()
      self.location = location
      self.consequent = conclusions
         
   def rif(self, position, index): 
      location = str(self.location + 'M') #notes and changes the location for later
      premises = copy.deepcopy(self.antecedent) #makes a copy of the premises
      conclusions = copy.deepcopy(self.consequent) #makes a copy of the conclusion
      mainprop = conclusions[position].split(" ") #splits the conditional into words
      del conclusions[position] #deletes the conditional
      ahead = " ".join(mainprop[0:index]) #puts the antecedent back together
      behind = " ".join(mainprop[index + 1:]) #puts the consequent back together
      premises.append(ahead) #puts the antecedent on with the premises
      conclusions.append(behind) #puts the consequent with the conclusions
      levelup = Sequent(self.name, location, premises, conclusions) #creates a placeholder sequent
      levelup.planter() #plants the parent
      self.location = location #alters the sequent
      self.antecedent = premises #alters the sequent 
      self.consequent = conclusions #alters the sequent
         
   def rneg(self, position, index): #See notes for lneg; they are the same except l and r are swapped in the natural places
      location = str(self.location + 'M')
      premises = copy.deepcopy(self.antecedent)
      conclusions = copy.deepcopy(self.consequent)
      mainprop = conclusions[position].split(" ")
      del conclusions[position]
      del mainprop[index]
      prop = " ".join(mainprop)
      premises.append(prop)
      levelup = Sequent(self.name, location, premises, conclusions)
      levelup.planter()
      self.location = location
      self.consequent = conclusions
      self.antecedent = premises
         
   def router(self, side, position, connective, index): #sends parser to whichever
      #decomposition function is appropriate, noting which side we're working with,
      #which proposition on that side, what the main connective is, and what space that
      #connective occupies in the propositon.
      if side == "left":
         if connective == "and":
            self.land(position, index)
         elif connective == "or":
            self.lor(position, index)
         elif connective == "implies":
            self.lif(position, index)
         elif connective == "not":
            self.lneg(position, index)
      elif side == "right":
         if connective == "and":
            self.rand(position, index)
         elif connective == "or":
            self.ror(position, index)
         elif connective == "implies":
            self.rif(position, index)
         elif connective == "not":
            self.rneg(position, index)

   def parser(self):
      ##currently locates the main connective of each antecedent of a sequent
      self.deparen()
      if self.atomcheck() == False:
         seqname = self.name
         premises = self.antecedent
         conclusions = self.consequent
         found = False
         index = []
         connective = []
         side = []
         position = -1
         if found == False:
            for propositions in self.antecedent:              #The purpose of this loop is to find the main connective
               if found == False:
                  position = position + 1
                  words = propositions.split(" ")
                  degree = 0              #number of open parentheses
                  num = -1                #becomes the index of the main connective in words
                  for word in words:
                     num = num + 1
                     if word in Connectives:
                        if degree == 0:
                           index = num  #locks on to the main connective
                           connective = word #which connective is it
                           side = "left" #antecedent or consequent
                           found = True
                     else:
                        letters = list(word)
                        for letter in letters:   #This loop keeps track of degrees. There should only
                                                 ##be one connective at degree 0, and it should be the main
                                                 ##connective.
                           if letter == "(":
                              degree = degree + 1
                           elif letter == ")":
                              degree = degree - 1
         if found == False:
            position = -1
            for conclusions in self.consequent:              #The purpose of this loop is to find
               ##the main connective
               if found == False:
                  position = position + 1
                  words = conclusions.split(" ")
                  degree = 0              #number of open parentheses
                  num = -1                #becomes the index of the main connective in words
                  for word in words:
                     num = num + 1
                     if word in Connectives:
                        if degree == 0:
                           index = num  #locks on to the main connective
                           connective = word
                           side = "right"
                           found = True
                     else:
                        letters = list(word)
                        for letter in letters:   #This loop keeps track of degrees. There should only
                           ##be one connective at degree 0, and it should be the main
                           ##connective.
                           if letter == "(":
                              degree = degree + 1
                           elif letter == ")":
                              degree = degree - 1
         if found == True: #If there is a connective, this sends the relevant info to the router.
            self.router(side, position, connective, index)
         elif found == False:
            for x in range(0, len(self.location)):
               if list(self.location)[x] == 'L': 
                  print ("There are no more complex sentences to decompose, and really you should never even see this message, so how did you get here? Someone must have broken something. \nYou can run the checker() function on this sequent to see what the current sequent looks like.")
      elif self.atomcheck == True:
         print ('This sequent is already atomic.')
      self.deparen()

   def checker(self): #Shows all the values of a given sequent
      print ('Sequent name, location, antecedent, consequent, atomic')
      print (self.name)
      print (self.location)
      print (self.antecedent)
      print (self.consequent)
      print (self.atomcheck())
      print ('')

   def main(self): #The main function
      self.deparen() #Cleans up the sequent
      if self.name not in Forest.keys(): #plants the tree if not planted already
         self.parser()
      while self.atomcheck() == False: #Decomposes the leftmost connective until there are no connectives to decompose
         self.parser()
      for x in range (0, len(self.location) - 1): #Recursive loop makes sure we hit all the rightward branching rules
         backstr = self.location[::-1] #Reverses the location so we can branch back
         if backstr[x] == 'L': #Every L location should have an associated R location
            newstr = backstr.replace('L', 'R', 1) #Changes only the most recent L to R (which is why we reversed the string)
            newloc = newstr[::-1] #Turns the location back around
            if x != 0: #If x is 0 (which happens when the most recent rule was a 2-parent rule), this next bit doesn't work
               newloc = newloc[:-x] #Removes everything after the R in location, since we only want the location up to the R
            self.location = newloc #edits the sequent so we can run our functions
            self.antecedent = Forest[self.name][newloc]['Antecedents'] #Gets the values from the relevant place in the tree
            self.consequent = Forest[self.name][newloc]['Consequents'] #Gets the values from the relevant place in the tree
            self.main() #Clears the tree starting from here.
                     
def debug(): #prints the forest in its (messy) entirety
   for x in Forest:
      print ('\'' + x + '\':')
      for y in Forest[x]:
         print('   ' + y + ':')
         for z in Forest[x][y]:
            print ('      ' + z + ':')
            for a in Forest[x][y][z]:
               print ('         ' + a)


def init(): #gets everything from the text file
   if os.path.exists('Forest.txt'): #Checks whether there is such a file locally
      f = open('Forest.txt', 'r') #opens it if there is
   else:
      f = open('Forest.txt', 'x') #creates one if not
   for line in f: #for each line in the file
      line = line.replace('\n', '') #removes all the new line commands
      line = line.replace('\'', '') #removes all the back slashes
      seq = line.split(';') #a list of the sequent's arguments
      ant = seq[2] #the antecedents
      con = seq[3] #the consequents
      ant = ant.replace('[', '') #removes the square brackets, which if kept would make for a proliferation of square brackets in the output
      ant = ant.replace(']', '')
      ant = ant.split(',') #turns ant from a string into a list
      con = con.replace('[', '')
      con = con.replace(']', '')
      con = con.split(',') #turns con from a string into a list
      Seq = Sequent((seq[0]), str(seq[1]), ant, con) #makes a sequent 
      Seq.main() #runs our program on the sequent
   
   


##
##testsuite = [killers, andseq, orseq, impseq, noseq, bigboy]
##
##for x in testsuite:
##   x.main()
##
##debug()
