# Requirements

- Python 3.7, with dependencies ```pip3 install click stanza```
- CoreNLP 4.0 (extracted to ./corenlp). https://stanfordnlp.github.io/CoreNLP/download.html

# Example commands:

## Formulas:

Print a list of sentences and their formulas.

```python3 src/cli.py formulas test/socrates.txt```

Example output:
```
Starting server with command: java -Xmx16G -cp ./corenlp/* edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 30000 -threads 5 -maxCharLength 100000 -quiet True -serverProperties corenlp_server-fb89f1665bd34819.props -preload tokenize,ssplit,pos,lemma,ner,parse,depparse,coref
[1]----------
If Socrates is a human , he is mortal . 
 If
  Socrates is a human 
  he is mortal . 
[2]----------
Socrates is mortal if he is a human . 
 if
  he is a human 
  Socrates is mortal . 
[3]----------
Socrates is mortal or Socrates is immortal . 
 or
  Socrates is mortal 
  Socrates is immortal 
[4]----------
Socrates is a human , and Socrates is not a dancer . 
 and
  Socrates is a human 
  not
   Socrates is a dancer 
[5]----------
Socrates and Plato are not immortal . 
 not
  Socrates and Plato are immortal . 
[6]----------
Therefore , Socrates is mortal . 
 Therefore , Socrates is mortal . 
[7]----------
If Socrates is a dancer and a human , then he is immortal . 
 If
  Socrates is a dancer and a human 
  then he is immortal . 
[8]----------
If Socrates is a human and a dancer but he is not immortal , then he is not a dancer and is mortal . 
 If
  but
   Socrates is a human and a dancer 
   not
    he is immortal 
  not
   then he is a dancer and is mortal . 
[9]----------
Should Socrates become a dancer , he will be immortal . 
 Should Socrates become a dancer , he will be immortal . 
[10]----------
If Socrates is a dancer and Plato is immortal then Socrates is immortal . 
 If
  and
   Socrates is a dancer 
   Plato is immortal 
  then Socrates is immortal . 
[11]----------
Socrates is a dancer , and if he is a dancer he is a mortal . 
 and
  Socrates is a dancer 
  if
   he is a dancer 
   he is a mortal 
[12]----------
Socrates is a human and Plato is a dancer and Socrates is not immortal . 
 and
  and
   Socrates is a human 
   Plato is a dancer 
  not
   Socrates is immortal 
[13]----------
Socrates is not immortal if Plato is tired . 
 if
  Plato is tired 
  not
   Socrates is immortal . 
[14]----------
All dancers are immortal and kind but some philosopher is mortal and mean . 
 but
  All dancers are immortal and kind 
  some philosopher is mortal and mean 
[15]----------
Socrates is not as immortal as a dancer would be and he certainly is not nimble , but he could be a dancer if he tried hard enough . 
 but
  and
   not
    Socrates is as immortal as a dancer would be 
   not
    he certainly is nimble 
  he could be a dancer if he tried hard enough 
```