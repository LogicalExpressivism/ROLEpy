import copy
import os
import stanza
from pprint import pprint
from google.protobuf.json_format import MessageToDict

os.environ["CORENLP_HOME"] = "./corenlp"

from stanza.server import CoreNLPClient
from stanza.server import to_text

# Helper function to print parseTrees more compactly.
def printTree(tree, indent=0):
    if len(tree.child) == 1 and len(tree.child[0].child) == 0:
        print("{}{} {}".format("  " * indent, tree.value, tree.child[0].value))
    else:
        print("{}{}".format("  " * indent, tree.value))
        for child in tree.child:
            printTree(child, indent + 1)

def subsentences(parsetree):
    ss = []
    for child in parsetree.child:
        ss.extend(subsentences(child))
    if parsetree.value == 'S':
        ss.append(parsetree)
    return ss

def parsetree_to_string(parsetree):
    string = ''
    for child in parsetree.child:
        string += parsetree_to_string(child)
    if len(parsetree.child) == 0:
        string += parsetree.value + ' '
    return string

class SequentInterface:
    def land(self):
        pass
    def lor(self):
        pass
    def lif(self):
        pass
    def lneg(self):
        pass
    def rand(self):
        pass
    def ror(self):
        pass
    def rif(self):
        pass
    def rneg(self):
        pass
    def parse(self):
        pass

class Formula:
    def __init__(self, tree, connective=None, left=None, right=None):
        self.tree = tree
        self.connective = connective
        self.left = left
        self.right = right
    
    def prettyPrint(self, indent=0):
        if self.connective == None:
            print('{}{}'.format(' ' * indent, parsetree_to_string(self.tree)))
        else:
            print('{}{}'.format(' ' * indent, self.connective))
            if self.left != None:
                self.left.prettyPrint(indent + 1)
            if self.right != None:
                self.right.prettyPrint(indent + 1)

# Sentence is the CoreNLP Sentence
class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence
    
    def parseFormulas(self):
        def hasInnerSbar(pt):
            if pt.value == 'SBAR':
                return True
            return any([hasInnerSbar(c) for c in pt.child])

        def firstidx(iter, val):
            for i, x in enumerate(iter):
                if x.value == val:
                    return True

        def parse(pt):
            if pt.value == 'ROOT':
                return parse(pt.child[0])
            if pt.value in ['S', '@S']:
                # Maybe @S/Punct pair
                for i, x in enumerate(pt.child):
                    if x.value in ['.', ',']:
                        return parse(pt.child[1 - i])
                # Maybe has @S
                atsidx = firstidx(pt.child, '@S')
                if atsidx != None:
                    ats = pt.child[atsidx]
                    other = pt.child[1 - atsidx]
                    if other.value == 'S':
                        # S/@S pair
                        ccidx = firstidx(ats.child, 'CC')
                        if ccidx != None:
                            return Formula(pt, ats.child[ccidx].child[0].value, parse(ats.child[1 - ccidx]), parse(other))
                    elif other.value == 'SBAR':
                        # SBAR/@S pair
                        inidx = firstidx(other.child, 'IN')
                        assert(inidx != None)
                        return Formula(pt, other.child[inidx].child[0].value, parse(other.child[1 - inidx]), parse(ats))
                    # elif hasInnerSbar(ats):
                        # TODO: Split at inner SBARS.
                # other pair
                return Formula(pt, None, None, None)
        return parse(self.sentence.binarizedParseTree)

document = open("test/socrates.txt", "r")

with CoreNLPClient(annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse', 'coref'], memory='4G', endpoint='http://localhost:9001') as client:
    text = document.read()
    doc = client.annotate(text)

    for sent in doc.sentence:
        print("--------------------------")
        print(to_text(sent))
        s = Sentence(sent)
        printTree(s.sentence.binarizedParseTree)
        f = s.parseFormulas()
        f.prettyPrint()