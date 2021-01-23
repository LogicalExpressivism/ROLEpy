from collections import namedtuple
from copy import copy
from functools import reduce, wraps, partial
from itertools import chain
from typing import Callable, List, NamedTuple, NoReturn, Optional, Union, Tuple, NewType

# import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout as layout
# import matplotlib.pyplot as plt

class Tm:
    """Abstract class for Terms."""
    def __repr__(self):
        raise NotImplementedError

# Singular Terms.

class St(Tm):
    """Singular Terms."""
    label: str

    def __init__(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return "{}{}".format(self.label, self.idx)

    def __eq__(self, other):
        if isinstance(other, St): return (self.label == other.label) and (self.idx == other.idx)
        return False

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

TmIdx, CdIdx, SqIdx, PrfIdx = NewType("TmIdx", int), NewType("CdIdx", int), NewType("SqIdx", int), NewType("PrfIdx", int)

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
        self.sequents: List[Tuple[CdIdx, CdIdx]] = [(0,0)]
        self.proofs: List[Tuple[SqIdx, List[SqIdx], str]] = []
        self.rules: List[Callable[[Sq], Prf]] = rules

    def insert_tm_idx(self, term: Tm) -> TmIdx:
        return insert_val_idx(self.terms, term)

    def insert_cd_idx(self, ced: Cd) -> CdIdx:
        return insert_val_idx(self.cedents, [self.insert_tm_idx(term) for term in ced.inner])

    def insert_sq_idx(self, sq: Sq) -> SqIdx:
        return insert_val_idx(self.sequents, (self.insert_cd_idx(sq.ant), self.insert_cd_idx(sq.suc)))

    def insert_prf_idx(self, prf: Prf) -> PrfIdx:
        return insert_val_idx(self.proofs, (self.insert_sq_idx(prf.sq), list(map(self.insert_sq_idx, prf.branches)), prf.label))

    def get_tm(self, tm: TmIdx) -> Tm:
        return self.terms[tm]
    
    def get_cd(self, cd: CdIdx) -> Cd:
        return Cd(list(map(self.get_tm, self.cedents[cd])))

    def get_sq(self, sq: SqIdx) -> Sq:
        ant, cons = self.sequents[sq]
        return Sq(self.get_cd(ant), self.get_cd(cons))

    def get_prf(self, prf: PrfIdx) -> Prf:
        s, b, l = self.proofs[prf]
        return Prf(self.get_sq(s), list(map(self.get_sq, b)), l)

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

    def calculate(self, sq: Sq) -> List[Prf]:
        return [self.insert_prf_idx(prf) for prf in filter(None, (rule(sq) for rule in self.rules))]

    # Note: due to the behaviour of this loop, all new sequents will be added to the end of the list,
    # and will therefore be included in the very same loop, and I believe it is not possible that we
    # miss any sequents.
    def calculate_all(self) -> None:
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
            
