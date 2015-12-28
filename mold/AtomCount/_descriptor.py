from .._base import Descriptor


class AtomCount(Descriptor):
    descriptor_defaults = [
        ('Atom',), ('HeavyAtom',),
        ('H',), ('B',), ('C',), ('N',), ('O',), ('S',), ('P',),
        ('F',), ('Cl',), ('Br',), ('I',), ('X',),
    ]

    @property
    def explicitHydrogens(self):
        return self.symbol in set(['H', 'Atom'])

    @property
    def descriptor_name(self):
        return 'n' + self.symbol

    @property
    def descriptor_key(self):
        return self.make_key(self.symbol)

    def __init__(self, symbol):
        self.symbol = symbol

        if symbol == 'X':
            self.f = self.calcX
        elif symbol == 'Atom' or symbol == 'HeavyAtom':
            self.f = self.calcAll
        else:
            self.f = self.calc

    def calcX(self, mol):
        X = set([9, 17, 35, 53, 85, 117])
        return sum((a.GetAtomicNum() in X for a in mol.GetAtoms()))

    def calc(self, mol):
        return sum((a.GetSymbol() == self.symbol for a in mol.GetAtoms()))

    def calcAll(self, mol):
        return mol.GetNumAtoms()

    def calculate(self, mol):
        return self.f(mol)

_descriptors = [AtomCount]
__all__ = [d.__name__ for d in _descriptors]
