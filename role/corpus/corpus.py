"""
Functions for working with our corpuses of sequent data.
"""
import json
import re
from typing import Iterable, Optional

def load_txt_sent_array(filename: str):
    with open(filename, "rt") as fp:
        data = fp.read()
        return data
    return None

kant_1 = load_txt_sent_array("role/corpus/kant/fpmm_1.txt")