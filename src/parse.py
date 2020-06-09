import copy
import os
import stanza
from pprint import pprint
from google.protobuf.json_format import MessageToDict

# Download and extract corenlp to ./corenlp to be able to use it.
os.environ["CORENLP_HOME"] = "./corenlp"

from stanza.server import CoreNLPClient
from stanza.server import to_text

from Sequent import Connective, Formula

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

def tokendict_to_string(parsetree):
    string = ''
    for child in parsetree['child']:
        string += tokendict_to_string(child)
    if len(parsetree['child']) == 0:
        string += parsetree['value'] + ' '
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

# class Formula:
#     def __init__(self, tree, connective=None, left=None, right=None):
#         self.tree = tree
#         self.connective = connective
#         self.left = left
#         self.right = right
    
#     def prettyPrint(self, indent=0):
#         if self.connective == None:
#             print('{}{}'.format(' ' * indent, tokendict_to_string(self.tree)))
#         else:
#             print('{}{}'.format(' ' * indent, self.connective))
#             if self.left != None:
#                 self.left.prettyPrint(indent + 1)
#             if self.right != None:
#                 self.right.prettyPrint(indent + 1)

# Sentence is the CoreNLP Sentence.
class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence

    def __str__(self):
        string = ''
        for token in self.sentence.token:
            string += token.originalText + ' '
        return string

    # Get a binarizedParseTree
    # Insert tokens into the parse tree.
    # Returns a recursive Dict structure.
    def binarizedParseTreeTokenDict(self):
        tokens = self.sentence.token
        bpt = self.sentence.binarizedParseTree
        idx = 0
        def rewriteNode(t):
            nonlocal idx, tokens
            children = [rewriteNode(child) for child in t.child]
            if len(children) == 0:
                assert len(tokens) > idx
                token = tokens[idx]
                idx += 1
                return {'value': t.value, 'child': children, 'token': token}
            return {'value': t.value, 'child': children}
        return rewriteNode(bpt)
    
    # Parse the binarizedParseTreeTokenDict
    # This would be better if we can use tregex from corenlp, but it does not work for me.
    def parseFormulasTokenDict(self):
        def hasInnerSbar(pt):
            if pt['value'] == 'S':
                return False
            if pt['value'] == 'SBAR':
                return True
            return any([hasInnerSbar(c) for c in pt['child']])

        def splitInnerSbar(pt):
            sbar = None
            rest = pt
            def recurse(t):
                nonlocal sbar
                for i, child in enumerate(t['child']):
                    if child['value'] == 'SBAR':
                        sbar = t['child'].pop(i)
                        return True
                    if hasInnerSbar(child):
                        return recurse(child)
                return False
            assert recurse(rest)
            return (sbar, rest)

        def hasInnerNot(pt):
            if pt['value'] == 'RB' and pt['child'][0]['value'] == 'not':
                return True
            return any([hasInnerNot(c) for c in pt['child']])

        def splitInnerNot(pt):
            rb = None
            rest = pt
            def recurse(t):
                nonlocal rb
                for i, child in enumerate(t['child']):
                    if child['value'] == 'RB' and child['child'][0]['value'] == 'not':
                        rb = t['child'].pop(i)
                        return True
                    if hasInnerNot(child):
                        return recurse(child)
                return False
            assert recurse(rest)
            return (rb, rest)

        def firstidx(iter, val):
            for i, x in enumerate(iter):
                if x['value'] == val:
                    return i
            return None

        def parse(pt):
            if pt['value'] == 'ROOT':
                return parse(pt['child'][0])
            if pt['value'] in ['S', '@S']:
                # Maybe @S/Punct pair
                for i, x in enumerate(pt['child']):
                    if x['value'] in ['.', ',']:
                        return parse(pt['child'][1 - i])
                # Maybe has @S
                atsidx = firstidx(pt['child'], '@S')
                if atsidx != None:
                    ats = pt['child'][atsidx]
                    other = pt['child'][1 - atsidx]
                    if other['value'] == 'S':
                        # S/@S pair
                        ccidx = firstidx(ats['child'], 'CC')
                        if ccidx != None:
                            conn = ats['child'][ccidx]['child'][0]['value']
                            if conn in ['and', 'but']:
                                return Formula(tokendict_to_string(pt), Connective.AND, parse(ats['child'][1 - ccidx]), parse(other))
                            elif conn == 'or':
                                return Formula(tokendict_to_string(pt), Connective.OR, parse(ats['child'][1 - ccidx]), parse(other))
                    elif other['value'] == 'SBAR':
                        # SBAR/@S pair
                        inidx = firstidx(other['child'], 'IN')
                        if inidx != None:
                            conn = other['child'][inidx]['child'][0]['value']
                            if conn.lower() == 'if':
                                return Formula(tokendict_to_string(pt), Connective.IMPLIES, parse(other['child'][1 - inidx]), parse(ats))
                    elif hasInnerSbar(ats):
                        # Split at inner SBARS.
                        sbar, rest = splitInnerSbar(pt)
                        inidx = firstidx(sbar['child'], 'IN')
                        conn = sbar['child'][inidx]['child'][0]['value']
                        if conn.lower() == 'if':
                            return Formula(tokendict_to_string(pt), Connective.IMPLIES, parse(sbar['child'][1 - inidx]), parse(rest))
                # other pair
                # should split propositions over subjects and VPs
                if hasInnerNot(pt):
                    # Split at inner RB 'not'
                    # Counts split VPs as whole phrases currently
                    rb, rest = splitInnerNot(pt)
                    conn = rb['child'][0]['value']
                    if conn == 'if':
                        return Formula(tokendict_to_string(pt), Connective.NOT, parse(rest), None)
                return Formula(tokendict_to_string(pt), None, None, None)
        return parse(self.binarizedParseTreeTokenDict())