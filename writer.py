## This allows us to easily add sequents to the forest
##
## Formatting notes:
## 1. Each sentence should be parenthesized separately from the connective: '((A) or (B)) and ((C) implies (D))'
## This makes sure we decompose only main connectives for each proposition
## 2. Case doesn't matter, but things end up looking nicer if you're at least consistent.
#######################################################

import os
import sequents


def add():
    name = [] #creates an empty variable for later
    while name == []: #loops until the user gives us a usable name
        try:
            name = input('Name of new sequent: ') 
        except:
            print ('Sorry, I didn\'t catch that. Please try again just using numbers and letters.') #prints this if anything other than a string is entered
    numant = -1 #creates a variable for the number of antecedents
    while numant < 0: #loops until the user gives us a usable number
        try:
            numant = int(input('Number of antecedents: '))
        except:
            print ( 'Sorry, I didn\'t catch that. Please try again using a natural number. ') #prints this if anything other than an integer is entered
        if numant < 0:
            print ( 'Sorry, but you can\'t have a negative amount of antecedents. Please try again using a natural number.') #prints this if the number entered is negative
    ant = [] #creates an empty variable for later
    for x in range (0, numant): #generates a prompt for each antecedent
        ant += input('Antecedent ' + str(x+1) + ': ') #user enters antecedent
        ant += ',' #adds commas to separate antecedents
    del ant[-1] #eliminates the last comma that was put there by the loop
    ant = ''.join(ant) #puts all the antecedents into a string
    numcon = -1 #This next bit is the same as for antecedents
    while numcon < 0: 
        try:
            numcon = int(input('Number of consequents: '))
        except:
            print ( 'Sorry, I didn\'t catch that. Please try again using a natural number. ')
        if numcon < 0:
            print ( 'Sorry, but you can\'t have a negative amount of antecedents. Please try again using a natural number.') 
    con = []
    for x in range (0, numcon):
        con += input('Consequent ' + str(x+1) + ': ')
        con += ','
    del con[-1]
    con = ''.join(con)
    newseq = str('\n' + name + ';M;[' + ant + '];[' + con + ']') #creates a sequent out of the gathered data
    f = open('Forest.txt', 'a') #opens the forest
    f.write(newseq) #adds the sequent to the forest
    f.close #closes the forest
    newseq = sequents.Sequent(name, 'M', ant, con)
    newseq.main() #processes the new sequent
    
