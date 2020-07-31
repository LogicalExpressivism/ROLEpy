import os
import sequents


def add():
    name = []
    while name == []:
        try:
            name = input('Name of new sequent: ')
        except:
            print ( 'Sorry, I didn\'t catch that. Please try again just using numbers and letters.' )
    numant = -1
    while numant < 0:
        try:
            numant = int(input('Number of antecedents: '))
        except:
            print ( 'Sorry, I didn\'t catch that. Please try again using a natural number. ')
    ant = []
    for x in range (0, numant):
        ant += input('Antecedent ' + str(x+1) + ': ')
        ant += ','
    del ant[-1]
    ant = ''.join(ant)
    ant = ant.replace(',', ', ')
    numcon = -1
    while numcon < 0:
        try:
            numcon = int(input('Number of consequents: '))
        except:
            print ( 'Sorry, I didn\'t catch that. Please try again using a natural number. ')
    con = []
    for x in range (0, numcon):
        con += input('Consequent ' + str(x+1) + ': ')
        con += ','
    del con[-1]
    con = ''.join(con)
    con = con.replace(',', ', ')
    newseq = str('\n' + name + ';M;[' + ant + '];[' + con + ']')
    f = open('Forest.txt', 'a')
    f.write(newseq)
    f.close
    newseq.sequents.main()
    
