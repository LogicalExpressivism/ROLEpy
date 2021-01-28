from collections import namedtuple
from copy import copy
from functools import reduce, wraps, partial
from itertools import chain
from typing import Callable, List, NamedTuple, NoReturn, Optional, Union, Tuple, NewType, TypeVar, Generic, Type

class Tm:
    """Abstract class for Terms."""
    def __repr__(self):
        raise NotImplementedError

class St(Tm):
    label: str

    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return "{}{}".format(self.label, self.idx)

    def __eq__(self, other):
        return (self.label == other.label) and (self.idx == other.idx) if isinstance(other, type(self)) else False

class Cn(Tm):
    """Connectives."""
    arity: int
    label: str

    def __init__(self, *tms: Tm):
        if len(tms) != self.arity:
            raise TypeError("This connective is of arity {}, but {} arguments were given.".format(self.arity, len(tms)))
        self.tms = tms

    def __repr__(self):
        return "{}({})".format(self.label, ", ".join(map(repr, self.tms)))

    def __eq__(self, other):
        if isinstance(other, Cn): return (self.label == other.label) and (self.tms == other.tms)
        return False

class Qn(Tm):
    """Quantifiers."""
    label: str
    bindto: type

    def __init__(self, x: type, fm: Tm):
        self.x = x
        self.fm = fm

    def __repr__(self):
        return "{} {}.{}".format(self.label, self.x, self.fm)

def define_singular_term(label) -> type:
    return type(label, (St,), {
        "label": label
    })

def define_connective(conn, arity) -> type:
    return type(conn, (Cn,), {
        "arity": arity,
        "label": conn,
    })

def define_quantifier(sym: str, bindto: type) -> type:
    return type(sym, (Qn,), {
        "label": sym,
        "bindto": bindto
    })

"""
In this section we defined cedents, sequents, and proofs.
"""

class Cd(Tuple[Tm, ...]):
    """Cedents are internally a list of terms."""
    # def __init__(self, inner: List[Tm]):
    #     self.inner = inner

    # def __copy__(self):
    #     return Cd(self.inner.copy())

    def __repr__(self):
        return ", ".join(map(repr, self))

class Sq(Tuple[Cd, Cd]):
    kind: str
    turnstile: str
    ant_restriction: Callable = lambda _, x: True
    suc_restriction: Callable = lambda _, x: True

    def __init__(self, sq: Tuple[Cd, Cd]):
        """Sequents are internally two cedents."""
        ant, suc = sq
        assert self.ant_restriction(ant) # pylint: disable=no-value-for-parameter
        assert self.suc_restriction(suc) # pylint: disable=no-value-for-parameter
        self.ant = ant
        self.suc = suc

    # def __copy__(self):
    #     return Sq(copy(self.ant), copy(self.suc))

    def __repr__(self):
        return "{} {} {}".format(self.ant, self.turnstile, self.suc)

class Prf:
    kind: str
    sq_restriction: Callable[[Sq], bool] = lambda _, x: True

    def __init__(self, sq: Sq, branches: List[Sq], label: str):
        """Proofs are internally a sequent, a list of sequents, and a label."""
        assert self.sq_restriction(sq) # pylint: disable=no-value-for-parameter
        assert all(self.sq_restriction(s) for s in branches) # pylint: disable=no-value-for-parameter
        self.sq = sq
        self.branches = branches
        self.label = label

    def __repr__(self):
        return "{} ==> {} ({})".format(self.sq, "; ".join(map(repr, self.branches)), self.label)

def define_sequent(
    kind: str,
    turnstile: str = "|~",
    ant_restriction = lambda _, x: True,
    suc_restriction = lambda _, x: True
    ) -> type:
    return type(kind, (Sq,), {
        "kind": kind,
        "turnstile": turnstile,
        "ant_restriction": ant_restriction,
        "suc_restriction": suc_restriction,
    })

def define_proof(kind, sq_restriction) -> type:
    return type(kind, (Prf,), {
        "label": kind,
        "sq_restriction": lambda _, x: True,
    })

TmIdx, CdIdx, SqIdx, PrfIdx = NewType("TmIdx", int), NewType("CdIdx", int), NewType("SqIdx", int), NewType("PrfIdx", int)

def insert_val_idx(l, v):
    for i, x in enumerate(l):
        if isinstance(v, List) and isinstance(x, List):
            if sorted(x) == sorted(v):
                return i
        elif isinstance(v, Tuple) and isinstance(x, Tuple) and len(v) == 3 and len(x) == 3:
            if v[0] == x[0] and sorted(v[1]) == sorted(x[1]):
                return i
        if x == v:
            return i
    l.append(v)
    return len(l) - 1

SqType, PrfType = TypeVar("SqType"), TypeVar("PrfType")

class Context(Generic[SqType, PrfType]):
    def __init__(self, sqtype: Type[SqType], prftype: Type[PrfType], rules: List):
        self.sqtype = sqtype
        self.prftype = prftype
        self.terms: List[Tm] = []
        self.cedents: List[List[TmIdx]] = [[]]
        self.sequents: List[Tuple[CdIdx, CdIdx]] = [(0,0)]
        self.proofs: List[Tuple[SqIdx, List[SqIdx], str]] = []
        self.rules: List[Callable[[Sq], Prf]] = rules

    def insert_tm_idx(self, term: Tm) -> TmIdx:
        return insert_val_idx(self.terms, term)

    def insert_cd_idx(self, cd: Cd) -> CdIdx:
        return insert_val_idx(self.cedents, [self.insert_tm_idx(term) for term in cd])

    def insert_sq_idx(self, sq: SqType) -> SqIdx:
        return insert_val_idx(self.sequents, (self.insert_cd_idx(sq.ant), self.insert_cd_idx(sq.suc)))

    def insert_prf_idx(self, prf: PrfType) -> PrfIdx:
        return insert_val_idx(self.proofs, (self.insert_sq_idx(prf.sq), list(map(self.insert_sq_idx, prf.branches)), prf.label))

    def get_tm(self, tm: TmIdx) -> Tm:
        return self.terms[tm]
    
    def get_cd(self, cd: CdIdx) -> Cd:
        return Cd(map(self.get_tm, self.cedents[cd]))

    def get_sq(self, sq: SqIdx) -> SqType:
        return self.sqtype(tuple(map(self.get_cd, self.sequents[sq])))

    def get_prf(self, prf: PrfIdx) -> PrfType:
        s, b, l = self.proofs[prf]
        return self.prftype(self.get_sq(s), tuple(map(self.get_sq, b)), l)

    def repr_tms(self) -> str:
        return ", ".join(map(repr, self.terms))

    def repr_inner_tms(self) -> str:
        return ", ".join(map(repr, (idx for idx, _ in enumerate(self.terms))))

    def repr_inner_cds(self) -> str:
        return ", ".join(map(repr, self.cedents))

    def repr_inner_sqs(self) -> str:
        return ", ".join("({}, {})".format(sq[0], sq[1]) for sq in self.sequents)

    def repr_inner_prfs(self) -> str:
        return ". ".join("{} => [{}] ({})".format(prf[0], ", ".join(map(repr, prf[1])), prf[2]) for prf in self.proofs)

    def try_into_sequent(self, sq: Tuple[Cd, Cd]) -> Optional[SqType]: # pylint: disable=unsubscriptable-object
        try:
            return self.sqtype(sq)
        except AssertionError:
            return None

    def try_into_proof(self, rule_result: Tuple[Tuple[Cd, Cd], Tuple[Tuple[Cd, Cd], ...], str]) -> Optional[PrfType]: # pylint: disable=unsubscriptable-object
        try:
            sq = self.try_into_sequent(rule_result[0])
            branches = tuple(map(self.try_into_sequent, rule_result[1]))
            assert sq is not None
            assert all(branch is not None for branch in branches)
            return self.prftype(sq, branches, rule_result[2])
        except AssertionError:
            return None

    def calculate(self, sq: Sq) -> List[PrfIdx]:
        return [self.insert_prf_idx(prf) for prf in filter(None, map(self.try_into_proof, filter(None, (rule(sq) for rule in self.rules))))]

    def calculate_all(self) -> None:
        for ant, suc in self.sequents:
            self.calculate((self.get_cd(ant), self.get_cd(suc)))
