from .calculi.lk import *

if __name__ == "__main__":
    test = Sq(Cd([A(1), And(A(1), A(2)), Not(A(2))]), Cd([Or(A(12), Not(A(2))), And(A(3), Not(And(A(1), A(4))))]))
    test2 = Sq(Cd([A(4), Or(A(2), Not(A(3))), A(5)]), Cd([A(6), And(A(1), A(2))]))
    test3 = Sq(Cd([Or(A(7), Not(Not(And(A(2), Or(A(9), Not(A(2))))))), A(9)]), Cd([A(6), A(10), A(11), A(12)]))
    print("Running on sequent:", test, test2)
    context = Context(Rules)
    context.insert_sq_idx(test)
    context.insert_sq_idx(test2)
    context.insert_sq_idx(test3)
    context.calculate_all()
    # print("\nInner terms:")
    # for i, t in enumerate(context.terms):
    #     print("{}\t{}".format(i, t))
    # print("\nInner cedents:")
    # for i, c in enumerate(context.cedents):
    #     print("{}\t{}\t\t{}".format(i, c, context.get_cd(i)))
    # print("\nInner sequents:")
    # for i, s in enumerate(context.sequents):
    #     print("{}\t{}\t\t{}".format(i, s, context.get_sq(s)))
    # print("\nInner proofs:")
    # for i, prf in enumerate(context.proofs):
    #     print("{}\t{}=>{}\t\t{}".format(i, prf[0], prf[1], prf[2]))
    print("\nTrying some relationships")
    for i, _ in enumerate(context.cedents):
        print("{}. {}".format(i, context.get_cd(i)))
        print("--------------")
        ant_of = [(j, s) for (j, s) in enumerate(context.sequents) if s[0] == i]
        suc_of = [(j, s) for (j, s) in enumerate(context.sequents) if s[1] == i]
        for idx, s in chain(ant_of, suc_of):
            print("\t{}. {}".format(idx, context.get_sq(idx)))
            prf_of = [(j, p) for (j, p) in enumerate(context.proofs) if idx in p[1]]
            for jdx, p in prf_of:
                print("\t\t{}. {}".format(jdx, context.get_prf(jdx)))
        print("")
    # print("\nNow plotting your graph.")
    # context.graph_prfs()