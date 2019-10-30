# This class wraps a 2D array and give us some additional functionalities (such as width, height and boundary checks)
# Although this class is hashable (can be used a key in a dictionary), it is not mutable for convenience so care should be taken whenever we modify its content

class Map2D:
    def __init__(self, array):
        # we take a copy to ensure that it doesn't modify or get modified by its source
        self._array = [[cell for cell in row] for row in array]
    
    @property
    def width(self):
        return len(self._array[0])
    
    @property
    def height(self):
        return len(self._array)
    
    # Support for indexing. "indices" must be an iterable with 2 elements (e.g. List, Tuple, Vector) 
    # it can be called using m[v] where v is a vector, list or tuple or m[x, y] where x and y are integers
    def __getitem__(self, indices):
        x, y = indices
        return self._array[y][x]

    def __setitem__(self, indices, value):
        x, y = indices
        self._array[y][x] = value
    
    # check if a vector is within the boundaries of the map
    def inside(self, indices):
        x, y = indices
        return 0 <= x < self.width and 0 <= y < self.height
    
    # support for iteration => e.g. for row in m:
    def __iter__(self):
        return iter(self._array)
    
    # Map2D is hashable although it is mutable. BE CAREFUL
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self._array))
    
    # Support for equality
    def __eq__(self, other: 'Map2D') -> bool:
        return self.width == other.width and self.height == other.height and all(all(c1 == c2 for c1, c2 in zip(r1, r2)) for r1, r2 in zip(self, other))