# Requirements

- Python 3.7, with dependencies ```pip3 install click stanza```
- CoreNLP 4.0 (extracted to ./corenlp). https://stanfordnlp.github.io/CoreNLP/download.html

# Example commands:

## Formulas:

```python3 src/cli.py formulas test/socrates.txt```

Example output:
```Starting server with command: java -Xmx16G -cp ./corenlp/* edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 30000 -threads 5 -maxCharLength 100000 -quiet True -serverProperties corenlp_server-ddd697ef01d54d8b.props -preload tokenize,ssplit,pos,lemma,ner,parse,depparse,coref
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
  Socrates is not a dancer 
[5]----------
Socrates and Plato are not immortal . 
 Socrates and Plato are not immortal . 
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
   he is not immortal 
  then he is not a dancer and is mortal . 
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
  Socrates is not immortal 
[13]----------
Socrates is not immortal if Plato is tired . 
 if
  Plato is tired 
  Socrates is not immortal . 
```