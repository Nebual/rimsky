class Vector:
    """ Represents a 2D vector
        Hashes like a len2 tuple
    """
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __add__(self, val):
        return Vector(self.x + val[0], self.y + val[1])
    
    def __sub__(self,val):
        return Vector(self.x - val[0], self.y - val[1])
    
    def __iadd__(self, val):
        self.x += val[0]
        self.y += val[1]
        return self
        
    def __isub__(self, val):
        self.x -= val[0]
        self.y -= val[1]
        return self
    
    def __div__(self, val):
        return Vector(self.x / val, self.y / val)
    
    def __mul__(self, val):
        return Vector(self.x * val, self.y * val)
    
    def __idiv__(self, val):
        self.x /= val
        self.y /= val
        return self
        
    def __imul__(self, val):
        self.x *= val
        self.y *= val
        return self
                
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise Exception("Invalid key to Vector")
        
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise Exception("Invalid key to Vector")
        
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
