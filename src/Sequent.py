from enum import Enum, auto
from copy import deepcopy
from pprint import pprint

class Connective(Enum):
    AND = auto()
    OR = auto()
    IMPLIES = auto()
    NOT = auto()

class Formula:
    def __init__(self, data, connective=None, left=None, right=None):
        self.data = data
        if connective == None:
            assert left == None
            assert right == None
        else:
            assert isinstance(connective, Connective)
        self.connective = connective
        self.left = left
        self.right = right

    def isAtomic(self):
        return self.connective == None

    def __str__(self):
        if self.connective == None:
            return "{}".format(self.data)
        if self.right == None:
            return "{}: {} {}".format(self.data, self.connective, self.left)
        return "{}: {} {} {}".format(self.data, self.left, self.connective, self.right)

class Sequent:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def isAtomic(self):
        for formula in self.antecedent:
            if not formula.isAtomic():
                return False
        for formula in self.consequent:
            if not formula.isAtomic():
                return False
        return True

    def __str__(self):
        string = ""
        for antecedent in self.antecedent:
            string += "{}\n".format(antecedent)
        string += "⊢\n"
        for consequent in self.consequent:
            string += "{}\n".format(consequent)
        return string

    def land(self, idx):
        antecedent = deepcopy(self.antecedent)
        consequent = deepcopy(self.consequent)
        f = antecedent.pop(idx)
        antecedent.extend([f.left, f.right])
        return [Sequent(antecedent, consequent)]

    def lor(self, idx):
        antecedent = deepcopy(self.antecedent)
        f = antecedent.pop(idx)
        antecedent2 = deepcopy(antecedent)
        consequent = deepcopy(self.consequent)
        consequent2 = deepcopy(self.consequent)
        antecedent.append(f.left)
        antecedent2.append(f.right)
        return [
            Sequent(antecedent, consequent),
            Sequent(antecedent2, consequent2)
        ]

    def limp(self, idx):
        antecedent = deepcopy(self.antecedent)
        f = antecedent.pop(idx)
        antecedent2 = deepcopy(antecedent)
        antecedent2.append(f.right)
        consequent = deepcopy(self.consequent)
        consequent.append(f.left)
        consequent2 = deepcopy(self.consequent)
        return [
            Sequent(antecedent, consequent),
            Sequent(antecedent2, consequent2)
        ]

    def lnot(self, idx):
        antecedent = deepcopy(self.antecedent)
        consequent = deepcopy(self.consequent)
        f = antecedent.pop(idx)
        consequent.append(f.left)
        return [Sequent(antecedent, consequent)]

    def rand(self, idx):
        antecedent = deepcopy(self.antecedent)
        antecedent2 = deepcopy(self.antecedent)
        consequent = deepcopy(self.consequent)
        f = consequent.pop(idx)
        consequent2 = deepcopy(consequent)
        consequent.append(f.left)
        consequent2.append(f.right)
        return [
            Sequent(antecedent, consequent),
            Sequent(antecedent2, consequent2)
        ]

    def ror(self, idx):
        antecedent = deepcopy(self.antecedent)
        consequent = deepcopy(self.consequent)
        f = consequent.pop(idx)
        consequent.extend([f.left, f.right])
        return [Sequent(antecedent, consequent)]

    def rimp(self, idx):
        antecedent = deepcopy(self.antecedent)
        f = antecedent.pop(idx)
        antecedent.append(f.left)
        consequent = deepcopy(self.consequent)
        consequent.append(f.right)
        return [
            Sequent(antecedent, consequent),
        ]

    def rnot(self, idx):
        antecedent = deepcopy(self.antecedent)
        consequent = deepcopy(self.consequent)
        f = consequent.pop(idx)
        antecedent.append(f.left)
        return [Sequent(antecedent, consequent)]

    def parse(self):
        for i, formula in enumerate(self.antecedent):
            if not formula.isAtomic():
                if formula.connective == Connective.AND:
                    return self.land(i)
                if formula.connective == Connective.OR:
                    return self.lor(i)
                if formula.connective == Connective.IMPLIES:
                    return self.limp(i)
                if formula.connective == Connective.NOT:
                    return self.lnot(i)
        print("No antecedents to parse")
        for i, formula in enumerate(self.consequent):
            if not formula.isAtomic():
                if formula.connective == Connective.AND:
                    return self.rand(i)
                if formula.connective == Connective.OR:
                    return self.ror(i)
                if formula.connective == Connective.IMPLIES:
                    return self.rimp(i)
                if formula.connective == Connective.NOT:
                    return self.rnot(i)
        print("No consequents to parse either!")

    def recursiveParse(self):
        if self.isAtomic():
            print("Got atom")
            print(str(self))
            return self
        print("Got complex sequent")
        print(str(self))
        return [self, [s.recursiveParse() for s in self.parse()]]

# test = Sequent(
#     [Formula('test', Connective.AND, Formula('test2', Connective.OR, Formula('A'), Formula('B')), Formula('C'))],
#     [Formula('test', Connective.OR, Formula('A'), Formula('test3', Connective.NOT, Formula('D')))]
# )

# pprint(test.recursiveParse())