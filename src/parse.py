import stanza

stanza.download('en')
en_nlp = stanza.Pipeline('en')

sentence = en_nlp("If Socrates is a human, he is mortal. Socrates is mortal if he is a human. Socrates is mortal or Socrates is immortal. Socrates is a human, and Socrates is not a dancer. Therefore, Socrates is mortal.")

for i, sent in enumerate(sentence.sentences):
    print("[Sentence {}]".format(i+1))
    for word in sent.words:
        print("{:12s}\t{:12s}\t{:6s}\t{:d}\t{:12s}".format(\
              word.text, word.lemma, word.pos, word.head, word.deprel))
    print("")