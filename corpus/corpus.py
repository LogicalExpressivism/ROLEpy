"""
Functions for working with our corpuses of sequent data.
"""
import json
import re
from nltk.tokenize import sent_tokenize, word_tokenize # type: ignore
from typing import Iterable, Optional

def load_txt_sent_array(filename: str):
    with open(filename, "rt") as fp:
        data = fp.read()
        return sent_tokenize(data)
    return None


if __name__ == "__main__":
    kant_sentences = load_txt_sent_array("corpus/kant/fpmm_1.txt")
    if kant_sentences is not None:
        for i, sentence in enumerate(kant_sentences):
            print("{}: {}".format(i, sentence))