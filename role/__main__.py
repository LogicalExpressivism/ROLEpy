from .calculus import Context, Cd
from itertools import chain
from tabulate import tabulate

def context_dump(context):
    print("\nInner terms:")
    print(tabulate((i, t) for i, t in enumerate(context.terms)))
    print("\nInner cedents:")
    print(tabulate((i, c, context.get_cd(i)) for i, c in enumerate(context.cedents)))
    print("\nInner sequents:")
    print(tabulate((i, s, context.get_sq(i)) for i, s in enumerate(context.sequents)))
    print("\nInner proofs:")
    print(tabulate((i, prf[0], prf[1], prf[2], context.get_prf(i)) for i, prf in enumerate(context.proofs)))


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
    context_dump(lkcontext)

    ljcontext = Context(LJSq, LJPrf, Rules)
    for sq in ljsqs:
        ljcontext.insert_sq_idx(sq)
    ljcontext.calculate_all()
    context_dump(ljcontext)
