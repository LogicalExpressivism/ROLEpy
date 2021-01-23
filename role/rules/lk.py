from functools import partial
from itertools import chain
from ..calculus import define_singular_term, define_connective, define_quantifier, Sq, Cd, Prf, Context
from .internal import u1, u2, b1, b2, b3, b4, b5, b6, instance_rule

A = define_singular_term("A")
X = define_singular_term("X")

And = define_connective("And", 2)
Or = define_connective("Or", 2)
Impl = define_connective("Impl", 2)
Not = define_connective("Not", 1)

# Here, rules are matching over their types. We could have done this by label or however else we wanted.
matcher = lambda x, y: isinstance(y, x)

LNot = instance_rule("ant", Not, "LNot")(u1)
RNot = instance_rule("suc", Not, "RNot")(u2)
LAnd1 = instance_rule("ant", And, "LAnd1")(b1)
LAnd2 = instance_rule("ant", And, "LAnd2")(b2)
RAnd = instance_rule("suc", And, "RAnd")(b3)
ROr1 = instance_rule("suc", Or, "ROr1")(b4)
ROr2 = instance_rule("suc", Or, "ROr2")(b5)
LOr = instance_rule("ant", Or, "LOr")(b6)

def Axiom(sq: Sq):
    return Prf(sq, [Sq(Cd([]), Cd([]))], "Axiom") if any(x == y for x in sq.ant.inner for y in sq.suc.inner) else None

Rules = [Axiom, LNot, RNot, LAnd1, LAnd2, RAnd, ROr1, ROr2, LOr]