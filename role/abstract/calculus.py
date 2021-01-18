from collections import namedtuple
from copy import copy, deepcopy
from dataclasses import dataclass
from first import first
from functools import reduce, wraps, partial
from typing import Callable, List, NamedTuple, NoReturn, Optional, Union, Tuple

class Tm:
    def depth(self) -> int:
        raise NotImplementedError

class A(Tm):
    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return "A{}".format(self.idx)
    
    def __eq__(self, other):
        if isinstance(other, A): return self.idx == other.idx
        return False

    def depth(self):
        return 0

class X(Tm):
    def __init__(self, idx: int):
        self.idx = idx
    
    def __repr__(self):
        return "X{}".format(self.idx)
    
    def __eq__(self, other):
        if isinstance(other, X): return self.idx == other.idx
        return False

    def depth(self):
        return 0

class Cn(Tm):
    arity: int
    label: str

    def __init__(self, *tms: List[Tm]):
        if len(tms) != self.arity:
            raise TypeError("This connective is of arity {}, but {} arguments were given.".format(self.arity, len(tms)))
        self.tms = tms

    def __repr__(self):
        return "{}({})".format(self.label, ", ".join(map(repr, self.tms)))

    def depth(self):
        return reduce(lambda x, y: x.depth() + y.depth(), self.tms) + 1

def define_connective(conn, arity) -> Cn:
    return type(conn, (Cn,), {
        "arity": arity,
        "label": conn,
    })

class Qn(Tm):
    label: str

    def __init__(self, x: X, fm: Tm):
        self.x = x
        self.fm = fm

    def __repr__(self):
        return "{} {}.{}".format(self.label, self.x, self.fm)

    def depth(self):
        return self.fm.depth() + 1

def define_quantifier(sym: str) -> Qn:
    return type(sym, (Qn,), {
        "label": sym
    })

And = define_connective("And", 2)
Or = define_connective("Or", 2)
Impl = define_connective("Impl", 2)
Not = define_connective("Not", 1)

AllAdd = define_quantifier("All+")
AllMult = define_quantifier("All*")
ExistAdd = define_quantifier("Exists+")
ExistsMult = define_quantifier("Exists*")

class Sq:
    def __init__(self, ant: List[Tm], suc: List[Tm]):
        self.ant = ant
        self.suc = suc

    def __copy__(self):
        return Sq(self.ant.copy(), self.suc.copy())

    def __repr__(self):
        return "{} |- {}".format(", ".join(map(repr, self.ant)), ", ".join(map(repr, self.suc)))

    def atomic(self):
        return any(x == y for x in self.ant for y in self.suc)

class Prf:
    def __init__(self, root: Sq, rl: str, branches: List["Prf"]):
        self.root = root
        self.rl = rl
        self.branches = branches

    def __repr__(self):
        return "{} => [{}] ({})".format(self.root, ". ".join(map(repr, self.branches)), self.rl)

MaybeSqs = Optional[List[Sq]] # pylint: disable=unsubscriptable-object

def axiom(sq: Sq) -> MaybeSqs:
    return [] if any(x == y for x in sq.ant for y in sq.suc) else None

def extractor(side, instance, label):
    def decorator(func):
        def wrapper(*args, **kwargs) -> MaybeSqs:
            match = first(id + 1 for id, x in enumerate(getattr(args[0], side)) if isinstance(x, instance) and x.label == label)
            if match is None: return None
            sq2 = copy(args[0])
            match = sq2.ant.pop(match - 1)
            return func(sq2, match, **kwargs)
        return wrapper
    return decorator

@extractor("ant", Cn, "Not")
def lnot(sq, match):
    sq.suc.append(match.tms[0])
    return [sq]

@extractor("suc", Cn, "Not")
def rnot(sq, match):
    sq.ant.append(match.tms[0])
    return [sq]

@extractor("ant", Cn, "And")
def land1(sq, match):
    sq.ant.append(match.tms[0])
    return [sq]

@extractor("ant", Cn, "And")
def land2(sq, match):
    sq.ant.append(match.tms[1])
    return [sq]

@extractor("suc", Cn, "And")
def rand(sq, match):
    sq2 = copy(sq)
    sq.suc.append(match.tms[0])
    sq2.suc.append(match.tms[1])
    return [sq, sq2]

@extractor("ant", Cn, "Impl")
def limpl(sq, match):
    sq2 = copy(sq)
    sq.suc.append(match.tms[0])
    sq2.ant.append(match.tms[1])
    return [sq, sq2]

# @TODO: There are many more calculus implementations than this.
def calculus(sq):
    result, label = None, None
    for name, rule in [
        ("Axiom", axiom),
        ("LNot", lnot),
        ("RNot", rnot),
        ("LAnd1", land1),
        ("RAnd2", land2),
        ("RAnd", rand),
        ("LImpl", limpl),
    ]:
        check = rule(sq)
        if check is not None:
            result, label = check, name
            break
    if result is None: return Prf(sq, "Nothing", [])
    return Prf(sq, label, list(map(calculus, result)))

def test1():
    test = And(A(1), Impl(A(1), A(2)))
    print(test)
    # print("Depth:", test.depth())
    try:
        test2 = And(A(1), A(2), A(3))
        print(test2)
    except TypeError as err:
        print("Got the correct error:", err)
    test3 = Sq([And(A(1), A(3)), Not(A(2)), Impl(A(1), A(2))], [])
    print(test3)
    # print("Depth:", test3.depth())
    print("Atomic" if test3.atomic() else "Nonatomic")
    test4 = lnot(test3)
    print(test4)
    test5 = Sq([A(1)], [A(1)])
    print(axiom(test5))

    test6 = calculus(test3)
    print(test6)

    # print("Depth:", test4.depth())

def tests():
    test1()

if __name__=="__main__":
    tests()