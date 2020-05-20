import stanza

class Formula:
    def __init__(self, sentence):
        self.sentence = sentence
    
    def hasConj(self) -> bool:
        for word in self.sentence.words:
            if word.pos == "SCONJ" or word.pos == "CCONJ":
                return True
        return False

    def allConjs(self):
        return [word for word in self.sentence.words if word.pos == "SCONJ" or word.pos == "CCONJ"]

    def subformulas(self):
        if not self.hasConj():
            return []
        pass

    

stanza.download('en')
en_nlp = stanza.Pipeline('en')

document = open("test/socrates.txt", "r")

parsed = en_nlp(document.read())

for i, sent in enumerate(parsed.sentences):
    print("[Sentence {}]".format(i+1))
    for word in sent.words:
        print("{}\t{:12s}\t{:12s}\t{:6s}\t{:d}\t{:12s}".format(\
              word.id, word.text, word.lemma, word.pos, word.head, word.deprel))
    print("")
    root = next((w for w in sent.words if w.head == 0), None)
    if root:
        print("Root: ({}) {}".format(root.id, root.text))
        print([word.text for word in sent.words if (int(word.head) == int(root.id) or int(word.id) == int(root.id))])
    sconj = next((w for w in sent.words if w.pos == "SCONJ"), None)
    if sconj:
        print("SCONJ: ({}) {} -> ({}) {}".format(sconj.id, sconj.text, sconj.head, sent.words[int(sconj.head)-1].text))
        print([word.text for word in sent.words if (int(word.head) == int(sconj.head) or int(word.id) == int(sconj.head))])
    cconj = next((w for w in sent.words if w.pos == "CCONJ"), None)
    if cconj:
        print("CCONJ: ({}) {} -> ({}) {}".format(cconj.id, cconj.text, cconj.head, sent.words[int(cconj.head)-1].text))
        print([word.text for word in sent.words if (int(word.head) == int(cconj.head) or int(word.id) == int(cconj.head))])
    print("")

# formulas = [Formula(s) for s in parsed.sentences]
# for f in formulas:
#     print(f.subformulas())

"""
Output:

[Sentence 1]
1       If              if              SCONJ   5       mark        
2       Socrates        Socrates        PROPN   5       nsubj       
3       is              be              AUX     5       cop         
4       a               a               DET     5       det         
5       human           human           ADJ     9       advcl       
6       ,               ,               PUNCT   9       punct       
7       he              he              PRON    9       nsubj       
8       is              be              AUX     9       cop         
9       mortal          mortal          ADJ     0       root        
10      .               .               PUNCT   9       punct       

Root: (9) mortal
['human', ',', 'he', 'is', 'mortal', '.']
SCONJ: (1) If -> (5) human
['If', 'Socrates', 'is', 'a', 'human']

[Sentence 2]
1       Socrates        Socrates        PROPN   3       nsubj       
2       is              be              AUX     3       cop         
3       mortal          mortal          ADJ     0       root        
4       if              if              SCONJ   8       mark        
5       he              he              PRON    8       nsubj       
6       is              be              AUX     8       cop         
7       a               a               DET     8       det         
8       human           human           ADJ     3       advcl       
9       .               .               PUNCT   3       punct       

Root: (3) mortal
['Socrates', 'is', 'mortal', 'human', '.']
SCONJ: (4) if -> (8) human
['if', 'he', 'is', 'a', 'human']

[Sentence 3]
1       Socrates        Socrates        PROPN   3       nsubj       
2       is              be              AUX     3       cop         
3       mortal          mortal          ADJ     0       root        
4       or              or              CCONJ   7       cc          
5       Socrates        Socrates        PROPN   7       nsubj       
6       is              be              AUX     7       cop         
7       immortal        immortal        ADJ     3       conj        
8       .               .               PUNCT   3       punct       

Root: (3) mortal
['Socrates', 'is', 'mortal', 'immortal', '.']
CCONJ: (4) or -> (7) immortal
['or', 'Socrates', 'is', 'immortal']

[Sentence 4]
1       Socrates        Socrates        PROPN   4       nsubj       
2       is              be              AUX     4       cop         
3       a               a               DET     4       det         
4       human           human           ADJ     0       root        
5       ,               ,               PUNCT   11      punct       
6       and             and             CCONJ   11      cc          
7       Socrates        Socrates        PROPN   11      nsubj       
8       is              be              AUX     11      cop         
9       not             not             PART    11      advmod      
10      a               a               DET     11      det         
11      dancer          dancer          NOUN    4       conj        
12      .               .               PUNCT   4       punct       

Root: (4) human
['Socrates', 'is', 'a', 'human', 'dancer', '.']
CCONJ: (6) and -> (11) dancer
[',', 'and', 'Socrates', 'is', 'not', 'a', 'dancer']

[Sentence 5]
1       Socrates        Socrates        PROPN   6       nsubj       
2       and             and             CCONJ   3       cc          
3       Plato           Plato           PROPN   1       conj        
4       are             be              AUX     6       cop         
5       not             not             PART    6       advmod      
6       immortal        immortal        ADJ     0       root        
7       .               .               PUNCT   6       punct       

Root: (6) immortal
['Socrates', 'are', 'not', 'immortal', '.']
CCONJ: (2) and -> (3) Plato
['and', 'Plato']

[Sentence 6]
1       Therefore       therefore       ADV     5       advmod      
2       ,               ,               PUNCT   5       punct       
3       Socrates        Socrates        PROPN   5       nsubj       
4       is              be              AUX     5       cop         
5       mortal          mortal          ADJ     0       root        
6       .               .               PUNCT   5       punct       

Root: (5) mortal
['Therefore', ',', 'Socrates', 'is', 'mortal', '.']

[Sentence 7]
1       If              if              SCONJ   5       mark        
2       Socrates        Socrates        PROPN   5       nsubj       
3       is              be              AUX     5       cop         
4       a               a               DET     5       det         
5       dancer          dancer          NOUN    13      advcl       
6       and             and             CCONJ   8       cc          
7       a               a               DET     8       det         
8       human           human           ADJ     5       conj        
9       ,               ,               PUNCT   13      punct       
10      then            then            ADV     13      advmod      
11      he              he              PRON    13      nsubj       
12      is              be              AUX     13      cop         
13      immortal        immortal        ADJ     0       root        
14      .               .               PUNCT   13      punct       

Root: (13) immortal
['dancer', ',', 'then', 'he', 'is', 'immortal', '.']
SCONJ: (1) If -> (5) dancer
['If', 'Socrates', 'is', 'a', 'dancer', 'human']
CCONJ: (6) and -> (8) human
['and', 'a', 'human']

[Sentence 8]
1       If              if              SCONJ   5       mark        
2       Socrates        Socrates        PROPN   5       nsubj       
3       is              be              AUX     5       cop         
4       a               a               DET     5       det         
5       human           human           ADJ     20      advcl       
6       and             and             CCONJ   8       cc          
7       a               a               DET     8       det         
8       dancer          dancer          NOUN    5       conj        
9       but             but             CCONJ   13      cc          
10      he              he              PRON    13      nsubj       
11      is              be              AUX     13      cop         
12      not             not             PART    13      advmod      
13      immortal        immortal        ADJ     5       conj        
14      ,               ,               PUNCT   20      punct       
15      then            then            ADV     20      advmod      
16      he              he              PRON    20      nsubj       
17      is              be              AUX     20      cop         
18      not             not             PART    20      advmod      
19      a               a               DET     20      det         
20      dancer          dancer          NOUN    0       root        
21      and             and             CCONJ   23      cc          
22      is              be              AUX     23      cop         
23      mortal          mortal          ADJ     20      conj        
24      .               .               PUNCT   20      punct       

Root: (20) dancer
['human', ',', 'then', 'he', 'is', 'not', 'a', 'dancer', 'mortal', '.']
SCONJ: (1) If -> (5) human
['If', 'Socrates', 'is', 'a', 'human', 'dancer', 'immortal']
CCONJ: (6) and -> (8) dancer
['and', 'a', 'dancer']

[Sentence 9]
1       Should          should          AUX     3       aux         
2       Socrates        Socrates        PROPN   3       nsubj       
3       become          become          VERB    10      advcl       
4       a               a               DET     5       det         
5       dancer          dancer          NOUN    3       xcomp       
6       ,               ,               PUNCT   10      punct       
7       he              he              PRON    10      nsubj       
8       will            will            AUX     10      aux         
9       be              be              AUX     10      cop         
10      immortal        immortal        ADJ     0       root        
11      .               .               PUNCT   10      punct       

Root: (10) immortal
['become', ',', 'he', 'will', 'be', 'immortal', '.']

[Sentence 10]
1       If              if              SCONJ   5       mark        
2       Socrates        Socrates        PROPN   5       nsubj       
3       is              be              AUX     5       cop         
4       a               a               DET     5       det         
5       dancer          dancer          NOUN    13      advcl       
6       and             and             CCONJ   9       cc          
7       Plato           Plato           PROPN   9       nsubj       
8       is              be              AUX     9       cop         
9       immortal        immortal        ADJ     5       conj        
10      then            then            ADV     13      advmod      
11      Socrates        Socrates        PROPN   13      nsubj       
12      is              be              AUX     13      cop         
13      immortal        immortal        ADJ     0       root        
14      .               .               PUNCT   13      punct       

Root: (13) immortal
['dancer', 'then', 'Socrates', 'is', 'immortal', '.']
SCONJ: (1) If -> (5) dancer
['If', 'Socrates', 'is', 'a', 'dancer', 'immortal']
CCONJ: (6) and -> (9) immortal
['and', 'Plato', 'is', 'immortal']
"""