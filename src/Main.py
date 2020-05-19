Connectives = ["and","or","implies","not"]

class Sequent:
   def __init__(self, antecedent, consequent):
      self.antecedent = antecedent
      self.consequent = consequent

   def deperen(self):                        #For each proposition in the sequent, removes the outermost perentheses (()).
      if self.antecedent != [""]:            #It causes problems if we pass an empty set into this
         bucket1 = self.antecedent               #holds onto antecedent
         self.antecedent = []                   #clears antecedent for overwriting
         for x in bucket1:                       
            y = list(x) #splits the proposition into characters
            if y[0] == "(" and y[-1] == ")":    #checks whether the outermost characters are in fact perentheses
               valid = True                     #Whether we want to remove outer brackets
               count = 0                        #number of open perens
               iterations = 0                   #times we've checked whether this character is a peren
               for a in y:
                  if valid == True:
                     iterations = iterations + 1  
                     if a == "(":                  
                        count = count + 1
                     if a == ")":
                        count = count - 1
                     if count <= 0:             #If we ever hit 0 before the very last close character in the sentence, we know something's wrong --- they're mismatched
                        if iterations < len(y):
                           valid = False
               if valid == True:
                  del y[0]
                  del y[-1]
                  z = "".join(y)                   #Puts the proposition back into sentence form
                  self.antecedent.append(z)        #repopulates the antecedent
               elif valid == False:
                  self.antecedent = bucket1
            else:
               self.antecedent = bucket1 #if there were no perentheses, this puts everything back as it was.

      if self.consequent != [""]:
         bucket2 = self.consequent               
         self.consequent = []                   
         for x in bucket2:                       
            y = list(x)                         
            if y[0] == "(" and y[-1] == ")":    
               valid = True                     
               count = 0                        
               iterations = 0                   
               for a in y:
                  if valid == True:
                     iterations = iterations + 1  
                     if a == "(":                  
                        count = count + 1
                     if a == ")":
                        count = count - 1
                     if count <= 0:             
                        if iterations < len(y):
                           valid = False
               if valid == True:
                  del y[0]
                  del y[-1]
                  z = "".join(y)                   
                  self.consequent.append(z)        
               elif valid == False:
                  self.consequent = bucket2
            else:
               self.consequent = bucket2  

   def parser(self): #WIP determines which decomposition function to run and runs it pretend this will work
      bucket = self.antecedent
      for x in bucket:
         pass

   def land(self): #this is currently doing what I thought parser would be doing --- currently locates (and prints) the main connective of each antecedent of a sequent
      antecedent = self.antecedent
      print (antecedent)
      self.antecedent = []
      connective = []
      for propositions in antecedent:              #The purpose of this loop is to find the main connective
         #print ("propositions = : " + str(propositions))
         words = propositions.split(" ")
         #print ("words = " + str(words))
         degree = 0
         #print ("starting degree = " + str(degree))
         num = -1
         #print ("starting num = " + str(num))
         for word in words:
            #print ("word = " + str(word))
            num = num + 1
            #print ("num = " + str(num))
            if word in Connectives:
               if degree == 0:
                  connective = num
                  #print ("new connectives = " + str(connective))
            else:
               letters = list(word)
               #print ("letters = " + str(letters))
               for letter in letters:
                  #print ("letter = " + str(letter))
                  if letter == "(":
                     degree = degree + 1
                  elif letter == ")":
                     degree = degree - 1
                  #print ("degree = " + str(degree))
         print ("connective = " + str(connective))
         print (words[int(connective)])
         
   def rand(self):
      pass

   def lor(self):
      pass

   def ror(self):
      pass

   def lif(self):
      pass

   def rif(self):
      pass

   def lneg(self):
      pass

   def rneg(self):
      pass
      
      
      
      
and_seq = Sequent(["(A and B)"],["(A and B)"])
or_seq = Sequent(["(C or D);"],["(C or D)"])
impl_seq = Sequent(["(E implies F)"],["(E implies F)"])
neg_seq = Sequent(["(not G)"],["(not G)"])
killers = Sequent(["(Socrates is human implies Socrates is mortal)", "((Socrates is human or Socrates is dancer) and (not (Socrates is dancer)))"],["(Socrates is mortal)"])
testseq = Sequent(["((A and B) and (C and D))"],["((A and B) and (C and D))"])


testseq.deperen()
testseq.land()
