"""
Functions for working with our corpuses of sequent data.
"""
import json
import re
from typing import List, Iterable, Optional

def load_txt_sent_array(filename: str):
    with open(filename, "rt") as fp:
        data = fp.read()
        return data
    return None

kant_1 = load_txt_sent_array("role/corpus/kant/fpmm_1.txt")
kant_2 = load_txt_sent_array("role/corpus/kant/fpmm_2.txt")

"""
Converting text files to feature grammars.
"""

from nltk.tree import Tree
from nltk.grammar import Nonterminal, Production, induce_pcfg
import os
import stanza
from stanza.server import CoreNLPClient
from stanza.protobuf import CoreNLP_pb2
os.environ["CORENLP_HOME"] = "./stanza_corenlp"

def start_server() -> CoreNLPClient:
    """Starts a CoreNLP server through Stanza and returns it."""
    stanza.install_corenlp(dir="./stanza_corenlp")
    return CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref', 'kbp', 'natlog', 'openie'],
        timeout=30000,
        memory='16G')

def start_stanza_server() -> stanza.Pipeline:
    stanza.download(lang='en', dir='./stanza_resources')
    return stanza.Pipeline(lang='en', dir='./stanza_resources')

def annotate_stanza_document_file(client: stanza.Pipeline, input: str, filename: str, output_format: str="serialized"):
    with open(filename, "wb") as file:
        ann = client(input)
        file.write(ann.to_dict())

def read_stanza_document_file(filename: str) -> stanza.Document:
    return stanza.Document.from_serialized(open(filename, "rb").read())

def annotate_document_file(client: CoreNLPClient, input: str, filename: str):
    with open(filename, "wb") as file:
        ann = client.annotate(input)
        file.write(ann.SerializeToString())

def read_document_file(filename: str, input_format: str="serialized") -> CoreNLP_pb2.Document:
    ann = CoreNLP_pb2.Document()
    return ann.ParseFromString(open(filename, "rb").read())

def build_trees(client, ann) -> List[Tree]: #takes an annotated dict
    trees = [sentence.parseTree.child[0] for sentence in ann.sentence]
    def recurse_build_tree(t):
        return Tree(t.value, map(recurse_build_tree, t.child)) if len(t.child) else t.value
    return list(map(recurse_build_tree, trees))

def extract_productions(trees: List[Tree]) -> List[Production]:
    return [production for tree in trees for production in tree.productions()]

def induce_grammar(productions: List[Production]):
    S = Nonterminal("S")
    return induce_pcfg(S, productions)