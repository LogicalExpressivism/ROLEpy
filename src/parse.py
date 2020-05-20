import stanza

stanza.download('en')
en_nlp = stanza.Pipeline('en')

doc = en_nlp("If Socrates is a human, he is mortal. Socrates is mortal if he is a human. Socrates is mortal or Socrates is immortal. Socrates is a human, and Socrates is not a dancer. Therefore, Socrates is mortal.")

for i, sent in enumerate(doc.sentences):
    print("[Sentence {}]".format(i+1))
    for word in sent.words:
        print("{:12s}\t{:12s}\t{:6s}\t{:d}\t{:12s}".format(\
              word.text, word.lemma, word.pos, word.head, word.deprel))
    print("")

"""Output:
[Sentence 1]
If              if              SCONJ   5       mark        
Socrates        Socrates        PROPN   5       nsubj       
is              be              AUX     5       cop         
a               a               DET     5       det         
human           human           ADJ     9       advcl       
,               ,               PUNCT   9       punct       
he              he              PRON    9       nsubj       
is              be              AUX     9       cop         
mortal          mortal          ADJ     0       root        
.               .               PUNCT   9       punct       

[Sentence 2]
Socrates        Socrates        PROPN   3       nsubj       
is              be              AUX     3       cop         
mortal          mortal          ADJ     0       root        
if              if              SCONJ   8       mark        
he              he              PRON    8       nsubj       
is              be              AUX     8       cop         
a               a               DET     8       det         
human           human           ADJ     3       advcl       
.               .               PUNCT   3       punct       

[Sentence 3]
Socrates        Socrates        PROPN   3       nsubj       
is              be              AUX     3       cop         
mortal          mortal          ADJ     0       root        
or              or              CCONJ   7       cc          
Socrates        Socrates        PROPN   7       nsubj       
is              be              AUX     7       cop         
immortal        immortal        ADJ     3       conj        
.               .               PUNCT   3       punct       

[Sentence 4]
Socrates        Socrates        PROPN   4       nsubj       
is              be              AUX     4       cop         
a               a               DET     4       det         
human           human           ADJ     0       root        
,               ,               PUNCT   11      punct       
and             and             CCONJ   11      cc          
Socrates        Socrates        PROPN   11      nsubj       
is              be              AUX     11      cop         
not             not             PART    11      advmod      
a               a               DET     11      det         
dancer          dancer          NOUN    4       conj        
.               .               PUNCT   4       punct       

[Sentence 5]
Therefore       therefore       ADV     5       advmod      
,               ,               PUNCT   5       punct       
Socrates        Socrates        PROPN   5       nsubj       
is              be              AUX     5       cop         
mortal          mortal          ADJ     0       root        
.               .               PUNCT   5       punct    
"""