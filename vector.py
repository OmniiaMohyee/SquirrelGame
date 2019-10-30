from collections.abc import Iterable, Collection
from typing import Any

# This is a simple vector class. It can be of any size, it supports indexing and access by ".x, .y, .z & .w".
# it also supports addition, subtraction and negation.
# This class is immutable and hashable so it can be used a key for a dictionary

class Vector:
    # Defining the attributes in a slot is a good optimization if the class is used a lot since it packs the class data more efficiently in memory
    __slots__ = ('components')

    # this is a static dictionary containing the index of each component (it is only used for __getattr__)
    _component_indices = {
        "x": 0,
        "y": 1,
        "z": 2,
        "w": 3
    }

    def __init__(self, *components):
        # since this class is immutable, we can only set attribute values by calling __setattr__ on the parent class
        super().__setattr__('components', components)
    
    # support for the len operator => e.g. len(v)
    def __len__(self) -> int:
        return len(self.components)
    
    # support for reading components using their index => e.g. v[0]
    def __getitem__(self, index: int) -> Any:
        if(index < len(self.components)):
            return self.components[index]
        else:
            raise IndexError(f'Index {index} is out of bounds for a Vector of Size {len(self.components)}')
    
    # since this class is immutable, we raise an error if anyone tries to set an item in it
    def __setitem__(self, index: int, value: Any):
        raise NotImplementedError("Vectors are immutable")
    
    # support for reading components using their names => e.g. v.x
    def __getattr__(self, name: str) -> Any:
        index = Vector._component_indices.get(name, -1)
        if index >= 0 and index < len(self.components):
            return self.components[index]
        else:
            raise AttributeError(f'{name} is not an attribute of a Vector of Size {len(self.components)}')
    
    # since this class is immutable, we raise an error if anyone tries to set an attribute in it
    def __setattr__(self, name: str, value: Any):
        raise NotImplementedError("Vectors are immutable")
    
    # since this class is immutable, we raise an error if anyone tries to delete an attribute in it
    def __delattr__(self, name: str):
        raise NotImplementedError("You cannot an attribute from a vector")

    def __hash__(self):
        # we can set the hash of a vector to be the hash of its component and a unique name to differentiate it from a regular tuple
        return hash(("Vector", self.components))
    
    # this adds support for iteration => e.g. for component in v:
    def __iter__(self):
        return iter(self.components)

    # support for addition with any iterable or scalar => v + w,  v + (1, 2), v + 2
    def __add__(self, other: Any) -> 'Vector':
        if isinstance(other, Iterable):
            return Vector(*[i+j for i, j in zip(self.components, other)])
        else:
            return Vector(*[i+other for i in self.components])

    # support for right-addition with non vector object => e.g. 1 + v,  [1, 2] + v
    def __radd__(self, other: Any) -> 'Vector':
        return self+other

    # support for subtraction with any iterable or scalar => v - w,  v - (1, 2), v - 2
    def __sub__(self, other: Any) -> 'Vector':
        if isinstance(other, Iterable):
            return Vector(*[i-j for i, j in zip(self.components, other)])
        else:
            return Vector(*[i-other for i in self.components])

    # support for right-subtraction with non vector object => e.g. 1 - v,  [1, 2] - v
    def __rsub__(self, other: Any) -> 'Vector':
        return (-self)+other
    
    # support for negation => e.g. -v
    def __neg__(self) -> 'Vector':
        return Vector(*[-i for i in self.components])
    
    # support for equality => e.g. v == w
    def __eq__(self, value: Collection) -> bool:
        return len(self) == len(value) and all(a==b for a, b in zip(self, value)) 
    
    # support for casting to string => e.g. str(v)
    def __str__(self) -> str:
        return f'({", ".join([str(i) for i in self.components])})'
    
    # support for object representation
    def __repr__(self) -> str:
        return f'Vector({", ".join([repr(i) for i in self.components])})'