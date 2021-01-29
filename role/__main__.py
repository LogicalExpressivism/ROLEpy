from .calculus import Context, Cd
from itertools import chain
from tabulate import tabulate
from itertools import zip_longest

def context_dump(context):
    print("\nInner terms:")
    print(tabulate((i, t) for i, t in enumerate(context.terms)))
    print("\nInner cedents:")
    print(tabulate((i, c, context.get_cd(i)) for i, c in enumerate(context.cedents)))
    print("\nInner sequents:")
    print(tabulate((i, s, context.get_sq(i)) for i, s in enumerate(context.sequents)))
    print("\nInner proofs:")
    print(tabulate((i, prf[0], prf[1], prf[2], context.get_prf(i)) for i, prf in enumerate(context.proofs)))

def compare_contexts(c1: Context, c2: Context):
    headers = ['Context 1', 'Context 2']
    print(tabulate(zip_longest(c1.terms, c2.terms), headers=headers), "\n")
    print(tabulate(map(lambda x: (
            x[0][1] if x[0] is not None else '',
            c1.get_cd(x[0][0]) if x[0] is not None else '',
            x[1][1] if x[1] is not None else '',
            c2.get_cd(x[1][0]) if x[1] is not None else ''
            ), zip_longest(enumerate(c1.cedents), enumerate(c2.cedents), fillvalue=None)
        ), headers=['(Internal)', 'Context 1', '(Internal)', 'Context 2']), "\n")
    print(tabulate(map(lambda x: (
            x[0][1] if x[0] is not None else '',
            '*' if x[0] is not None and any(proof for proof in c1.proofs if proof[0] == x[0][0] and proof[2] == 'Axiom') else '',
            c1.get_sq(x[0][0]) if x[0] is not None else '',
            x[1][1] if x[1] is not None else '',
            '*' if x[1] is not None and any(proof for proof in c2.proofs if proof[0] == x[1][0] and proof[2] == 'Axiom') else '',
            c2.get_sq(x[1][0]) if x[1] is not None else '',
            ), zip_longest(enumerate(c1.sequents), enumerate(c2.sequents), fillvalue=None)
        ), headers=['(Internal)', '', 'Context 1', '(Internal)', '', 'Context 2']), "\n")
    # Derive a map such that the index of a term in c1 is mapped to the index of the same term in c2.

if __name__ == "__main__":
    from role.rules import A, X, Not, And, Or, Impl, LKSq, LKPrf, LJSq, LJPrf, Rules

    sequents = [
        (Cd([A(1), And(A(1), A(2)), Not(A(2))]), Cd([Impl(A(12), Not(A(2)))])),
        (Cd([A(4), Or(Impl(X(2), A(10)), Not(A(3))), A(5)]), Cd([And(A(1), A(2))])),
        (Cd([Or(A(7), Not(Not(And(A(2), Or(A(9), Not(A(2))))))), A(9)]), Cd([A(12)]))
        ]
    lksqs = [LKSq(sq) for sq in sequents]
    ljsqs = [LJSq(sq) for sq in sequents]
    lkcontext = Context(LKSq, LKPrf, Rules)
    for sq in lksqs:
        lkcontext.insert_sq_idx(sq)
    lkcontext.calculate_all()
    ljcontext = Context(LJSq, LJPrf, Rules)
    for sq in ljsqs:
        ljcontext.insert_sq_idx(sq)
    ljcontext.calculate_all()
    compare_contexts(lkcontext, ljcontext)