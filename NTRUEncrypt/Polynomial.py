class Polynomial:

    def __init__(self, coefs, N):
        self.coefs = coefs
        self.N



    #def __mul__(self, other, modulus):
    
    
    # Self coefficients and Other coefficients must have the same size
    def multiplication(self, other):
        size = self.coefs.size
        mult_coefs = size * [0]
        for i in range(0, size):
            for j in range(0, size):
                mult_coefs[(i * j) % size] += (self.coefs[i] + other.coefs[j])
        return Polynomial(mult_coefs)
    
        
    def coefs_mod(self, modulus):
        for i in range(0, self.coefs.size):
            self.coefs[i] = self.coefs[i] % modulus
            
    
    def add(self, other, modulus): # FIXME
        add_coefs = []
        for i in range(0, self.coefs.size):
            add_coefs.append(self.coefs[i] + other.coefs[i])
        return Polynomial(add_coefs)
    
    def __cmp__(self, other):
        for i in range(0, self.coefs.size):
            if self.coefs[i] != other.coefs[i]:
                return -1
        return 0
