class Polynomial:
    
    def __init__(self, coefs):
        self.coefs = coefs
        
    # Self coefficients and Other coefficients must have the same size
    def __mul__(self, other):
        size = len(self.coefs)
        mult_coefs = size * [0]
        for i in range(size):
            for j in range(size):
                mult_coefs[(i + j) % size] += (self.coefs[i] * other.coefs[j])
        return Polynomial(mult_coefs)
    
    def __add__(self, other):
        add_coefs = []
        for i in range(0, len(self.coefs)):
            add_coefs.append(self.coefs[i] + other.coefs[i])
        return Polynomial(add_coefs)
    
    def __cmp__(self, other):
        for i in range(0, len(self.coefs)):
            if self.coefs[i] != other.coefs[i]:
                return -1
        return 0
    
    def __sub__(self, other):
        sub_coefs = []
        for i in range (len(self.coefs)):
            sub_coefs.append(self.coefs[i] - other.coefs[i])
        return Polynomial(sub_coefs)

    def coefs_mod(self, modulus):
        for i in range(0, len(self.coefs)):
            self.coefs[i] = self.coefs[i] % modulus

    def degree(self):
        for i in range(len(self.coefs), 0, -1):
            if self.coefs[i] != 0:
                return i

    def division(self, other):
        quotient = []
        remainder = Polynomial(self.coefs[:])
        end = [0] * self.coefs.size
        while remainder != end and remainder.degree() >= other.degree():
            temp = remainder[remainder.degree()] / other[other.degree()]
            quotient += temp
            remainder -= temp * other
        return [quotient, remainder]