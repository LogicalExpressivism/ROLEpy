from copy import deepcopy
from first import first
from typing import List, Optional, Tuple, NamedTuple

class RoleError(BaseException):
    pass

class Formula:
    def __init__(self, data: Optional[str] = None, conn: Optional[str] = None, first: Optional["Formula"] = None, second: Optional["Formula"] = None):
        if data is None:
            if (conn is None) or (first is None):
                raise RoleError("A formula with no data must have at least a unary connective and a formula.")
        else:
            if (conn is not None) or (first is not None) or (second is not None):
                raise RoleError("A formula with data must not have a connective nor subformula.")
        self.data = data
        self.conn = conn
        self.first = first
        self.second = second

    def __eq__(self, other):
        if isinstance(other, Formula):
            if self.data is None:
                return (self.conn == other.conn) and (self.first == other.first) and (self.second == other.second)
            return self.data == other.data
        return False
                    

    def __deepcopy__(self, memo):
        first = None if self.first is None else deepcopy(self.first)
        second = None if self.second is None else deepcopy(self.second)
        return Formula(self.data, self.conn, first, second)

    def __repr__(self):
        if self.data is None:
            if self.second is None:
                return "{} {}".format(self.conn, self.first)
            return "{} {} {}".format(self.first, self.conn, self.second)
        return self.data

    def isUnary(self):
        return self.first is not None and self.second is None

    def isBinary(self):
        return self.first is not None and self.second is not None

class Sequent:
    def __init__(self, left, right):
        self.left: List[Formula] = left
        self.right: List[Formula] = right

    def __repr__(self):
        return "{} |~ {}".format(", ".join(map(str, self.left)), ", ".join(map(str, self.right)))

def match_left(condition):
    def matcher(sequent):
        found, left, right = None, sequent.left, sequent.right
        for i, formula in enumerate(sequent.left):
            if condition(formula):
                found = i
                break
        return None if found is None else (left.pop(found), Sequent(left, right))
    return matcher

def match_right(condition):
    def matcher(sequent):
        found, left, right = None, sequent.left, sequent.right
        for i, formula in enumerate(sequent.right):
            if condition(formula):
                found = i
                break
        return None if found is None else (right.pop(found), Sequent(left, right))
    return matcher

def u1(formula, sequent):
    left, right = sequent.left, sequent.right
    left.append(formula.first)
    return Sequent(left, right)

def u2(formula, sequent):
    left, right = sequent.left, sequent.right
    right.append(formula.first)
    return Sequent(left, right)

def b1(formula, sequent):
    left, right = sequent.left, sequent.right
    left.extend([formula.first, formula.second])
    return Sequent(left, right)

def b2(formula, sequent):
    left, right = sequent.left, sequent.right
    left.append(formula.first)
    right.append(formula.second)
    return Sequent(left, right)

def b3(formula, sequent):
    left, right = sequent.left, sequent.right
    left.append(formula.second)
    right.append(formula.first)
    return Sequent(left, right)

def b4(formula, sequent):
    left, right = sequent.left, sequent.right
    right.extend([formula.first, formula.second])
    return Sequent(left, right)

def isNot(formula):
    return formula.conn == "not" and formula.isUnary()

def isAnd(formula):
    return formula.conn == "and" and formula.isBinary()

def isOr(formula):
    return formula.conn == "or" and formula.isBinary()

def isImp(formula):
    return formula.conn == "imp" and formula.isBinary()

def lneg(sequent):
    match = match_left(isNot)(sequent)
    return None if match is None else u2(*match)

def rneg(sequent):
    match = match_right(isNot)(sequent)
    return None if match is None else u1(*match)

def land(sequent):
    match = match_left(isAnd)(sequent)
    return None if match is None else b1(*match)

def limp(sequent):
    match = match_left(isImp)(sequent)
    return None if match is None else 

def test_formulas():
    a, b = Formula("A"), Formula("B")
    a_and_b = Formula(conn="/\\", first=deepcopy(a), second=deepcopy(b))
    a_imp_b = Formula(conn="->", first=deepcopy(a), second=deepcopy(b))
    return [a, b, a_and_b, a_imp_b]
    
def test_01():
    print("Test 1.")
    a, b, a_and_b, a_imp_b = test_formulas()

    fails = 0
    try:
        _ = Formula("C", "and")
    except RoleError:
        fails += 1
    try:
        _ = Formula(None, "or", None, "D")
    except RoleError:
        fails += 1
    try:
        _ = Formula("E", None, "A", None)
    except RoleError:
        fails += 1
    try:
        _ = Formula("F", None, None, "G")
    except RoleError:
        fails += 1
    print("Invalid formulas fail as expected." if fails == 4 else "Invalid formulas may be constructed, failing test.")

    for x in [a, b, a_and_b, a_imp_b]:
        print(x)
    
def test_02():
    print("Test 2.")
    a, b, _, a_imp_b = test_formulas()
    s = Sequent([a, a_imp_b], [b])
    print(s)

if __name__ == "__main__":
    test_01()
    test_02()