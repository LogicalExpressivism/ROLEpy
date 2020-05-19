Connectives = ["and","or","implies","not"]

class Sequent:
   def __init__(self, antecedent, consequent):
      self.antecedent = antecedent
      self.consequent = consequent

   def deperen(self):                        #For each proposition in the sequent, removes the
      ##outermost perentheses (()).
      if self.antecedent != [""]:            #It causes problems if we pass an empty set into
         ##this
         premises = self.antecedent               #holds onto antecedent
         self.antecedent = []                   #clears antecedent for overwriting
         for premise in premises:                       
            letters = list(premise) #splits the proposition into characters
            if letters[0] == "(" and letters[-1] == ")":    #checks whether the outermost characters are
               ##in fact perentheses
               valid = True                     #Whether we want to remove outer brackets
               count = 0                        #number of open perens
               iterations = 0                   #times we've checked whether this character
               ##is a peren
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
                  newpremise = "".join(letters)                   #Puts the proposition back into sentence
                  ##form
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
            if letters[0] == "(" and letters[-1] == ")":    #checks whether the outermost characters are
               ##in fact perentheses
               valid = True                     #Whether we want to remove outer brackets
               count = 0                        #number of open perens
               iterations = 0                   #times we've checked whether this character
               ##is a peren
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

   def land(self, position, index):
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = premises[position].split(" ")
      del premises[position]
      ahead = " ".join(mainprop[0:index])
      behind = " ".join(mainprop[index + 1:])
      self.antecedent.append(ahead)
      self.antecedent.append(behind)
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
      print ("Applied Left-And")
      
   def lor(self, position, index):
      print ("lor: position = " + str(position) + " index = " + str(index))
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = premises[position]
      del premises[position]

      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #

   def lif(self, position, index):
      print ("lif: position = " + str(position) + " index = " + str(index))
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = premises[position]
      del premises[position]
      
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
         
   def lneg(self, position, index):
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = premises[position].split(" ")
      del premises[position]
      behind = " ".join(mainprop[index + 1:])
      self.consequent.append(behind)
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
      print ("Applied Left-Not")
         
   def rand(self, position, index):
      print ("rand: position = " + str(position) + " index = " + str(index))
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = conclusions[position]
      del conclusions[position]
      
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
         
   def ror(self, position, index):
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = conclusions[position].split(" ")
      del conclusions[position]
      ahead = " ".join(mainprop[0:index])
      behind = " ".join(mainprop[index + 1:])
      self.consequent.append(ahead)
      self.consequent.append(behind)
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
      print ("Applied Right-Or")
         
   def rif(self, position, index):
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = conclusions[position].split(" ")
      del conclusions[position]
      ahead = " ".join(mainprop[0:index])
      behind = " ".join(mainprop[index + 1:])
      self.antecedent.append(ahead)
      self.consequent.append(behind)
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
      print ("Applied Right-If")
         
   def rneg(self, position, index):
      conclusions = self.consequent #stores consequent for later
      self.consequent = []          #
      premises = self.antecedent    #stores premises for later
      self.antecedent = []          #
      mainprop = conclusions[position].split(" ")
      del conclusions[position]
      behind = " ".join(mainprop[index + 1:])
      self.antecedent.append(behind)
      for x in premises:
         self.antecedent.append(x)
      for x in conclusions:         #Returns consequent
         self.consequent.append(x)  #
      print ("Applied Right-Not")
         
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

   def parser(self): #this is currently doing what I thought parser would be doing ---
      ##currently locates (and prints) the main connective of each antecedent of a sequent
      self.deperen()
      found = False
      index = []
      connective = []
      side = []
      position = -1
      if found == False:
         for propositions in self.antecedent:              #The purpose of this loop is to find
            ##the main connective
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
      
      if found == True:
         self.router(side, position, connective, index)
      elif found == False:
         print ("There are no more complex sentences to decompose")

      
      
and_seq = Sequent(["(A and B)"],["(A and B)"])
or_seq = Sequent(["(C or D)"],["(C or D)"])
impl_seq = Sequent(["(E implies F)"],["(E implies F)"])
neg_seq = Sequent(["(not G)"],["(not G)"])
killers = Sequent(["(Socrates is human implies Socrates is mortal)", "((Socrates is human or Socrates is dancer) and (not (Socrates is dancer)))"],["(Socrates is mortal)"])
testseq = Sequent(["F", "((A and B) and (A and B))"],["((C or D) or (C or D))"])



