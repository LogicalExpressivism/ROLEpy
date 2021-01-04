"""Higher Order Sequents.

The idea is to work with higher order rules in order to track more information about non-axiomatic sequents.
And to use that to track information about quantified sequent structures.
"""
from typing import List

class Ob:
    pass

class Tm(Ob):
    """The term superclass. Terms are things like variables and functions."""
    def __init__(self):
        pass

class Var(Tm):
    """Variables are any string."""
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, Var) else False

class Fn(Tm):
    """Functions are terms which have as many arguments are their specified arity."""
    def __init__(self, name: str, args: List[Tm]):
        self.name = name
        self.args = args
    
    def is_const(self):
        return len(self.args) == 0

class Fm(Ob):
    """Formulas are things like predicate symbols, connectives, and quantifiers."""
    def __init__(self):
        pass

    def is_sentence(self, bindings = []):
        if isinstance(self, Pr):
            return all(x in bindings for x in self.args)
        if isinstance(self, Cn):
            return all(x.is_sentence(bindings) for x in self.args)
        if isinstance(self, Qn):
            assert self.var not in bindings
            bindings.append(self.var)
            return self.fm.is_sentence(bindings)
        if isinstance(self, Var):
            return self.name in bindings
        if isinstance(self, Fn):
            return all(x.is_sentence(bindings) for x in self.args)
        return False

class Pr(Fm):
    """Predicates are formulas as many terms as their specified arity that designate relations or propositions."""
    def __init__(self, name: str, args: List[Var]):
        self.name = name
        self.args = args

    def is_prop_var(self):
        return len(self.args) == 0

class Cn(Fm):
    """Connectives take formulae as arguments."""
    def __init__(self, name: str, args: List[Fm]):
        self.name = name
        self.args = args

class Qn(Fm):
    """Quantifiers take a variable to bind and a formula to bind over."""
    def __init__(self, name: str, var: str, fm: Fm):
        self.name = name
        self.var = var
        self.fm = fm

    def __repr__(self):
        return "{} {}.{}".format(self.name, self.var, self.fm)

Cedent = List[Ob]

class Sq:
    def __init__(self, ant: Cedent, suc: Cedent):
        self.ant = ant
        self.suc = suc
