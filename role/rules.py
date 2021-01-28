from copy import deepcopy
from functools import wraps
from typing import Callable, List, Optional, Literal, Tuple
from role import calculus
from enum import Enum

class Side(Enum):
    ANT = 0
    SUC = 1

def instance_rule(side: Side, instance: type, label: str): # pylint: disable=unsubscriptable-object
    """
    This function is a decorator which composes over the internal rule representation.
    
    This will define an internal rule where the exchange rule is implicit and unlabeled.
    It takes a side ("ant" or "suc"), an instance to search for, and a label for the rule.
    The decorator then decorates a function which takes a sequent (without the matched term) and
    the matched term, and uses this function to derive the proof's branches. The sequent given
    is a copy that is to be modified and returned.

    You can use it as a decorator or a higher-order function:
    ```
    @instance_rule("ant", Not, "LNot")
    def lnot(s: Sequent, t: Not):
        s.suc.inner.append(t.tms[0])
        return s

    def rnot(s: Sequent, t: Not):
        s.ant.inner.append(t.tms[0])
        return s

    RNot = instance_rule("suc", Not, "RNot")(rnot)
    
    Rules = [lnot, RNot]
    ```
    """
    def decorator(func: Callable[[Tuple[calculus.Cd, calculus.Cd], calculus.Tm], List[Tuple[calculus.Cd, calculus.Cd]]]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Tuple[Tuple[calculus.Cd, calculus.Cd], List[Tuple[calculus.Cd, calculus.Cd]], str]]: # pylint: disable=unsubscriptable-object
            sq = args[0]
            match = None
            for id, x in enumerate(sq[side.value]):
                if match is None:
                    if isinstance(x, instance):
                        match = id
                        break
            else:
                return None
            match, rest = \
                (sq[0][match], (calculus.Cd(s for i, s in enumerate(sq[0]) if i != match), sq[1])) \
                if side.value == Side.ANT.value else \
                (sq[1][match], (sq[0], calculus.Cd(s for i, s in enumerate(sq[1]) if i != match)))
            return (sq, func(rest, match), label)
        return wrapper
    return decorator

def assert_arity(arity: int):
    """Helper decorator to bail if any matched connective has the wrong arity.

    This would mean that something is wrong in the code.
    """
    def decorator(func: Callable[[Tuple[calculus.Cd, calculus.Cd], calculus.Tm], List[Tuple[calculus.Cd, calculus.Cd]]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert len(args[1].tms) == arity
            return func(*args, **kwargs)
        return wrapper
    return decorator

@assert_arity(1)
def un_a(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ ((*sq[0], x.tms[0]), sq[1]) ]

@assert_arity(1)
def un_s(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ (sq[0], (*sq[1], x.tms[0])) ]

@assert_arity(2)
def bin_1a(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ ((*sq[0], x.tms[0]), sq[1]) ]

@assert_arity(2)
def bin_1s(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ (sq[0], (*sq[1], x.tms[0])) ]

@assert_arity(2)
def bin_2a(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ ((*sq[0], x.tms[1]), sq[1]) ]

@assert_arity(2)
def bin_2s(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ (sq[0], (*sq[1], x.tms[1])) ]

@assert_arity(2)
def bin_1a1_2a2(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ ((*sq[0], x.tms[0]), sq[1]), ((*sq[0], x.tms[1]), sq[1]) ]

@assert_arity(2)
def bin_1a1_2s2(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ ((*sq[0], x.tms[0]), sq[1]), (sq[0], (*sq[1], x.tms[1])) ]

@assert_arity(2)
def bin_1s1_2a2(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ (sq[0], (*sq[1], x.tms[0])), ((*sq[0], x.tms[1]), sq[1]) ]
    
@assert_arity(2)
def bin_1s1_2s2(sq: Tuple[calculus.Cd, calculus.Cd], x: calculus.Cn) -> List[Tuple[calculus.Cd, calculus.Cd]]:
    return [ (sq[0], (*sq[1], x.tms[0])), (sq[0], (*sq[1], x.tms[1])) ]

A = calculus.define_singular_term("A")
X = calculus.define_singular_term("X")

And = calculus.define_connective("And", 2)
Or = calculus.define_connective("Or", 2)
Impl = calculus.define_connective("Impl", 2)
Not = calculus.define_connective("Not", 1)

LKSq = calculus.define_sequent("LKSq", "|~LK", lambda _, x: True, lambda _, x: True)
LKPrf = calculus.define_proof("LKPrf", lambda _, x: isinstance(x, LKSq))

LJSq = calculus.define_sequent("LJSq", "|~LJ", suc_restriction=lambda _, x: len(x) <= 1)
LJPrf = calculus.define_proof("LJPrf", lambda _, x: isinstance(x, LJSq))

LNot = instance_rule(Side.ANT, Not, "LNot")(un_s)
RNot = instance_rule(Side.SUC, Not, "RNot")(un_a)
LAnd1 = instance_rule(Side.ANT, And, "LAnd1")(bin_1a)
LAnd2 = instance_rule(Side.ANT, And, "LAnd2")(bin_2a)
RAnd = instance_rule(Side.SUC, And, "RAnd")(bin_1s1_2s2)
ROr1 = instance_rule(Side.SUC, Or, "ROr1")(bin_1s)
ROr2 = instance_rule(Side.SUC, Or, "ROr2")(bin_2s)
LOr = instance_rule(Side.ANT, Or, "LOr")(bin_1a1_2a2)
LImpl = instance_rule(Side.ANT, Impl, "LImpl")(bin_1s1_2a2)
RImpl = instance_rule(Side.SUC, Impl, "RImpl")(bin_1a1_2s2)

def Axiom(sq: Tuple[calculus.Cd, calculus.Cd]):
    return (sq, [(calculus.Cd(), calculus.Cd())], "Axiom") if any(x == y for x in sq[0] for y in sq[1]) else None

Rules = [Axiom, LNot, RNot, LAnd1, LAnd2, RAnd, ROr1, ROr2, LOr, LImpl, RImpl]