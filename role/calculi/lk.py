from functools import partial
from itertools import chain
from ..calculus import define_singular_term, define_connective, define_quantifier, cnrule, matcher, u1, u2, b1, b2, b3, b4, b5, b6, Sq, Cd, Prf, Context

A = define_singular_term("A")
X = define_singular_term("X")

And = define_connective("And", 2)
Or = define_connective("Or", 2)
Impl = define_connective("Impl", 2)
Not = define_connective("Not", 1)

LNot = cnrule("ant", partial(matcher, Not), "LNot")(u1)
RNot = cnrule("suc", partial(matcher, Not), "RNot")(u2)
LAnd1 = cnrule("ant", partial(matcher, And), "LAnd1")(b1)
LAnd2 = cnrule("ant", partial(matcher, And), "LAnd2")(b2)
RAnd = cnrule("suc", partial(matcher, And), "RAnd")(b3)
ROr1 = cnrule("suc", partial(matcher, Or), "ROr1")(b4)
ROr2 = cnrule("suc", partial(matcher, Or), "ROr2")(b5)
LOr = cnrule("ant", partial(matcher, Or), "LOr")(b6)

def Axiom(sq: Sq):
    return Prf(sq, [Sq(Cd([]), Cd([]))], "Axiom") if any(x == y for x in sq.ant.inner for y in sq.suc.inner) else None

Rules = [Axiom, LNot, RNot, LAnd1, LAnd2, RAnd, ROr1, ROr2, LOr]