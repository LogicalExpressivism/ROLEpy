from .corpus import kant_1
from discopy import Ty, Word
import os
import stanza
from stanza.server import CoreNLPClient

os.environ["CORENLP_HOME"] = "./stanza_corenlp"
if not os.path.isdir("./stanza_resources"):
    stanza.download(dir="./stanza_resources")
if not os.path.isdir("./stanza_corenlp"):
    stanza.install_corenlp(dir="./stanza_corenlp")

def all_words(d):
    return [word for sent in d.sentences for word in sent.words]

def sort_by_arg(w, arg):
    d = dict()
    for word in w:
        d.setdefault(getattr(word, arg), []).append(word)
    return d

def print_sorted(d, arg, print_args=['text', 'lemma']):
    for key, val in sort_by_arg(all_words(d), arg).items():
        print("Key:", key)
        print("----------")
        for word in val:
            print(*[getattr(word, a) for a in print_args])
        print("")

if __name__ == "__main__":
    with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
        timeout=30000,
        memory='16G') as client:
        ann = client.annotate(kant_1)
        