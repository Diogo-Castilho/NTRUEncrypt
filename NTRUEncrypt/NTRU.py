from sage.all import *

class NTRU:
    
    def __init__(self, level):
        if level == 0:
            self.N = 11
            self.q = 32
            self.p = 3
        elif level == "test":
            self.N = 11
            self.q = 32
            self.p = 3
            self.R = PolynomialRing(QQ, 'x')
            x = self.R.gen()
            mock = self.test()
            self.f = -1 + x + x**2 - x**4 + x**6 + x**9 -x**10
            self.fp = mock[0]
            self.fq = mock[1]
            self.h = mock[2]
            self.g = -1 + x**2 + x**3 + x**5 - x**8 - x**10
        else:
            self.N = 503
            self.q = 256
            self.p = 3
        
    def generate_random_pol(self, lower, upper, N):
        coefs = []
        for i in range(N):
            coefs.append(int(random() * (upper - lower + 1)) + lower)
        return self.R(coefs)
    
    def create_keys(self):
        self.R = PolynomialRing(QQ, 'x')
        x = self.R.gen()
        gcd = 0
        while gcd != 1:
            self.f = self.generate_random_pol(-1,1, self.N)
            #self.f = -1 + x + x**2 - x**4 + x**6 + x**9 -x**10
            print(self.f)
            self.g = self.generate_random_pol(-1,1, self.N)
            extended_gcd = xgcd(x**self.N -1, self.f)
            gcd = extended_gcd[0]
            u = extended_gcd[1]
            v = extended_gcd[2]
        self.fp = self.mod(v, self.p)
        self.fq = self.mod(v, self.q)
        self.h = self.recenter(self.mul(self.p * self.fq, self.g),self.q)
        
    def test(self):
        self.R = PolynomialRing(QQ, 'x')
        x = self.R.gen()
        poly_a = -1 + x + x**2 - x**4 + x**6 + x**9 -x**10
        poly_b = -1 + x**2 + x**3 + x**5 - x**8 - x**10
        temp = x**11 -1
        extended_gcd = xgcd(temp, poly_a)
        gcd = extended_gcd[0]
        u = extended_gcd[1]
        v = extended_gcd[2]
        fp = self.mod(v, 3)
        fq = self.mod(v, 32)
        yetanother = 3 *fq
        print(yetanother)
        why = self.mul(yetanother, poly_b)
        print(why)
        h = self.recenter(why, 32)
        result = [fp, fq, h]
        return result
    
    def cipher(self, message, h):
        x = self.R.gen()
        random_pol = self.generate_random_pol(-1,1, self.N)
        #random_pol = -1 + x**2 + x**3 + x**4 - x**5 - x**7
        message_poly = self.mapping(self.encode(message))
        #message_poly = -1 + x**3 - x**4 - x**8 + x**9 + x**10
        print("message_poly")
        print(message_poly)
        temp = self.mul(h, random_pol)
        secret = self.mod(temp + message_poly, self.q)
        return secret
    
    def decipher(self, secret):
        print(secret)
        a = self.recenter(self.mul(secret, self.f), self.q)
        print(a)
        b = self.recenter(a, self.p)
        print(b)
        c = self.mul(self.fp, b)
        print(c)
        c = self.recenter(c, self.p)
        return c
        
    def mod(self, poly, num):
        coefs = poly.list()
        for i in range(len(coefs)):
            coefs[i] = Mod(coefs[i], num)
        return self.R(coefs)
    
    def recenter(self, poly, num):
        coefs = poly.list()
        limit = num//2
        for i in range(len(coefs)):
            coefs[i] = Mod(coefs[i], num)
            if coefs[i] > limit:
                coefs[i] = int(coefs[i]) - num
        return self.R(coefs)
    
    def mul(self, poly_a, poly_b): #FIXME
        coefs_a = poly_a.list()
        coefs_b = poly_b.list()
        mult_coefs = self.N * [0]
        for i in range(len(coefs_a)):
            for j in range(len(coefs_b)):
                mult_coefs[(i + j) % self.N] += (coefs_a[i] * coefs_b[j])
        return self.R(mult_coefs)
    
    
    def encode(self, message):
        bit_list = []
        for char in message:
            bits = bin(ord(char))[2:]
            bits = '00000000'[len(bits):] + bits
            bit_list.extend([int(bit) for bit in bits])
        print("bit_array:")
        print(bit_list)
        filler = 0
        temp_list = bit_list + [filler] * 3
        grouped_list = [temp_list[n:n + 3] for n in range(0, len(bit_list), 3)]
        return grouped_list
    
    def decode(grouped_list):
        bit_list = []
        for group in grouped_list:
            bit_list += group
        length = len(bit_list)
        filler_len = length % 8
        if filler_len != 0:
            bit_list = bit_list[:- filler_len]
        message = ''
        for index in range(len(bit_list) // 8):
            byte = bit_list[index * 8: (index + 1) * 8]
            message += chr(int(''.join([str(bit) for bit in byte]), 2))
        return message
    
    def mapping(self, bits_list):
        co_list = []
        for bits in bits_list:
            if bits == [0, 0, 0]:
                co_list.extend((0, 0))
            elif bits == [0, 0, 1]:
                co_list.extend((0, 1))
            elif bits == [0, 1, 0]:
                co_list.extend((0, -1))
            elif bits == [0, 1, 1]:
                co_list.extend((1, 0))
            elif bits == [1, 0, 0]:
                co_list.extend((1, 1))
            elif bits == [1, 0, 1]:
                co_list.extend((1, -1))
            elif bits == [1, 1, 0]:
                co_list.extend((-1, 0))
            elif bits == [1, 1, 1]:
                co_list.extend((-1, 1))
        print(co_list)
        return self.R(co_list)
    
    def inverse_mapping(self, co_list):
        bit_list = []
        for co in co_list:
            if co == [0, 0]:
                bit_list.append([0, 0, 0])
            elif co == [0, 1]:
                bit_list.append([0, 0, 1])
            elif co == [0, -1]:
                bit_list.append([0, 1, 0])
            elif co == [1, 0]:
                bit_list.append([0, 1, 1])
            elif co == [1, 1]:
                bit_list.append([1, 0, 0])
            elif co == [1, -1]:
                bit_list.append([1, 0, 1])
            elif co == [-1, 0]:
                bit_list.append([1, 1, 0])
            elif co == [-1, 1]:
                bit_list.append([1, 1, 1])
        return bit_list
    
    def group(self, list):
        co_list = []
        for i in range(len(0, list, 2)):
            co_list.append([list[i], list[i + 1]])
        return co_list
        
    
    # def decipher(message):
