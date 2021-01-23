from collections import namedtuple
from copy import copy
from functools import reduce, wraps, partial
from itertools import chain
from typing import Callable, List, NamedTuple, NoReturn, Optional, Union, Tuple

# import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout as layout
# import matplotlib.pyplot as plt

class Tm:
    """Abstract class for Terms."""
    def depth(self) -> int:
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

# Singular Terms.

class St(Tm):
    label: str

    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return "{}{}".format(self.label, self.idx)

    def __eq__(self, other):
        if isinstance(other, St): return (self.label == other.label) and (self.idx == other.idx)
        return False

# Compound terms.

class Cn(Tm):
    """Connectives."""
    arity: int
    label: str

    def __init__(self, *tms: List[Tm]):
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
        "label": label,
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

class Cd:
    """Cedents are internally a list of terms."""
    def __init__(self, inner: List[Tm]):
        self.inner = inner

    def __copy__(self):
        return Cd(self.inner.copy())

    def __repr__(self):
        return ", ".join(map(repr, self.inner))

class Sq:
    """Sequents are internally two cedents."""
    def __init__(self, ant: Cd, suc: Cd):
        self.ant = ant
        self.suc = suc

    def __copy__(self):
        return Sq(copy(self.ant), copy(self.suc))

    def __repr__(self):
        return "{} |~ {}".format(self.ant, self.suc)

class Prf:
    """Proofs are internally a sequent, a list of sequents, and a label."""
    def __init__(self, sq: Sq, branches: List[Sq], label: str):
        self.sq = sq
        self.branches = branches
        self.label = label

    def __repr__(self):
        return "{} ==> {} ({})".format(self.sq, "; ".join(map(repr, self.branches)), self.label)

"""
This section defines an internal representation of rules.
"""

def cnrule(side, condition: Callable[[Tm], bool], label: str):
    """This function is a decorator which compose over the internal rule representation."""
    def decorator(func: Callable[[Sq, Tm], List[Sq]]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[List[Prf]]: # pylint: disable=unsubscriptable-object
            assert side in ["ant", "suc"]
            sq = copy(args[0])
            matchid = None
            for id, x in enumerate(getattr(sq, side).inner):
                if condition(x):
                    matchid = id
                    break
            else:
                return None
            match = getattr(sq, side).inner.pop(matchid)
            return Prf(args[0], func(sq, match), label)
        return wrapper
    return decorator

def assert_arity(arity: int):
    """Helper decorator to bail if any matched connective has the wrong arity.

    This would mean that something is wrong in the code.
    """
    def decorator(func: Callable[[Sq, Tm], List[Sq]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(args[1])
            assert len(args[1].tms) == arity
            return func(*args, **kwargs)
        return wrapper
    return decorator

"""
These internal rules are underlying rules. We might have some connectives that use the same decomposition rules as another.

These functions take a sequent and connective, and return a list of sequents (the decomposed versions).
"""

@assert_arity(1)
def u1(sq: Sq, x: Cn) -> List[Sq]:
    sq.suc.inner.append(x.tms[0])
    return [sq]

@assert_arity(1)
def u2(sq: Sq, x: Cn) -> List[Sq]:
    sq.ant.inner.append(x.tms[0])
    return [sq]

@assert_arity(2)
def b1(sq: Sq, x: Cn) -> List[Sq]:
    sq.ant.inner.append(x.tms[0])
    return [sq]

@assert_arity(2)
def b2(sq: Sq, x: Cn) -> List[Sq]:
    sq.ant.inner.append(x.tms[1])
    return [sq]
    
@assert_arity(2)
def b3(sq: Sq, x: Cn) -> List[Sq]:
    sq2 = copy(sq)
    sq.suc.inner.append(x.tms[0])
    sq2.suc.inner.append(x.tms[1])
    return [sq, sq2]
    
@assert_arity(2)
def b4(sq: Sq, x: Cn) -> List[Sq]:
    sq.suc.inner.append(x.tms[0])
    return [sq]
    
@assert_arity(2)
def b5(sq: Sq, x: Cn) -> List[Sq]:
    sq.suc.inner.append(x.tms[1])
    return [sq]
    
@assert_arity(2)
def b6(sq: Sq, x: Cn) -> List[Sq]:
    sq2 = copy(sq)
    sq.ant.inner.append(x.tms[0])
    sq2.ant.inner.append(x.tms[1])
    return [sq, sq2]

# Here, rules are matching over their types. We could have done this by label or however else we wanted.
matcher = lambda x, y: isinstance(y, x)

TmIdx, CdIdx, SqIdx, PrfIdx = int, int, int, int

def insert_val_idx(l, v):
    for i, x in enumerate(l):
        if x == v:
            return i
    l.append(v)
    return len(l) - 1

class Context:
    def __init__(self, rules: List):
        self.terms: List[Tm] = []
        self.cedents: List[List[TmIdx]] = [[]]
        self.sequents: List[(CdIdx, CdIdx)] = [(0,0)]
        self.proofs: List[(SqIdx, List[SqIdx], str)] = []
        # I have set the list of rules in the initializer, but we can convert this to an argument later.
        self.rules = rules

    def insert_tm_idx(self, term: Tm) -> TmIdx:
        return insert_val_idx(self.terms, term)

    def insert_cd_idx(self, ced: Cd) -> CdIdx:
        return insert_val_idx(self.cedents, [self.insert_tm_idx(term) for term in ced.inner])

    def insert_sq_idx(self, sq: Sq) -> SqIdx:
        return insert_val_idx(self.sequents, (self.insert_cd_idx(sq.ant), self.insert_cd_idx(sq.suc)))

    def insert_prf_idx(self, prf: Prf) -> PrfIdx:
        return insert_val_idx(self.proofs, (self.insert_sq_idx(prf.sq), list(map(self.insert_sq_idx, prf.branches)), prf.label))

    def get_tm(self, tm: TmIdx):
        return self.terms[tm]
    
    def get_cd(self, cd: CdIdx):
        return Cd(list(map(self.get_tm, self.cedents[cd])))

    def get_sq(self, sq: SqIdx): # pylint: disable=unsubscriptable-object
        ant, cons = self.sequents[sq]
        return Sq(self.get_cd(ant), self.get_cd(cons))

    def get_prf(self, prf: PrfIdx):
        s, b, l = self.proofs[prf]
        return Prf(self.get_sq(s), list(map(self.get_sq, b)), l)

    def repr_tms(self):
        return ", ".join(map(repr, self.terms))

    def repr_inner_tms(self):
        return ", ".join(map(repr, (idx for idx, _ in enumerate(self.terms))))

    def repr_inner_cds(self):
        return ", ".join(map(repr, self.cedents))

    def repr_inner_sqs(self):
        return ", ".join("({}, {})".format(sq[0], sq[1]) for sq in self.sequents)

    def repr_inner_prfs(self):
        return ". ".join("{} => [{}] ({})".format(prf[0], ", ".join(map(repr, prf[1])), prf[2]) for prf in self.proofs)

    def calculate(self, sq: Sq):
        return [self.insert_prf_idx(prf) for prf in filter(None, (rule(sq) for rule in self.rules))]

    # Note: due to the behaviour of this loop, all new sequents will be added to the end of the list,
    # and will therefore be included in the very same loop, and I believe it is not possible that we
    # miss any sequents.
    def calculate_all(self):
        for i, _ in enumerate(self.sequents):
            self.calculate(self.get_sq(i))

    # def graph_prfs(self):
    #     g = nx.MultiDiGraph()
    #     g.add_edges_from((source, target) for (source, targets, _) in self.proofs for target in targets)
    #     g = nx.subgraph(g, nx.ancestors(g, 0))
    #     # @TODO: In progress attempt at fixing nodes that aren't sources or aren't targets of any edge at
    #     # different sides of the plot.
    #     # no_ancestors = []
    #     # no_descendants = []
    #     # others = []

    #     # napos = (1,-1)
    #     # naposdelta = 2. / len(no_ancestors)
    #     # ndpos = (-1,-1)
    #     # ndposdelta = 2. / len(no_descendants)
    #     # for node in g.nodes():
    #     #     if len(nx.ancestors(g, node)) == 0:
    #     #         no_ancestors[node] = napos
    #     #         napos = (napos[0], napos[1] + naposdelta)
    #     #         continue
    #     #     if len(nx.descendants(g, node)) == 0:
    #     #         no_descendants[node] = ndpos
    #     #         ndpos = (ndpos[0], ndpos[1] + ndposdelta)
    #     #         continue
    #     #     others[node] = (0,0)
    #     pos = nx.spring_layout(g,
    #         k=1,
    #         scale=4,
    #         # pos=[(n, p) for (n, p) in dicts.items() for dicts in [no_ancestors, no_descendants, others]],
    #         # fixed=[n for n in dicts.keys() for dicts in [no_ancestors, no_descendants]]
    #         )
        
    #     plt.figure(figsize=(10,10))
    #     options = {
    #         "with_labels": True,
    #         "edgecolors": "black",
    #         "edge_color": "black",
    #         "width": 1,
    #         "linewidths": 1,
    #         "node_size": 100,
    #         "node_color": "pink",
    #         "alpha": 0.9,
    #     }
    #     nx.draw(g, pos=pos, **options,
    #         labels={s:self.get_sq(s) for s in g.nodes()}
    #         )
    #     # nx.draw_networkx_edge_labels(g,pos,
    #     #     edge_labels={(source, target):rule for (source, targets, rule) in self.proofs for target in targets},
    #     #     font_color='red')
    #     plt.axis('off')
    #     plt.show()
            
