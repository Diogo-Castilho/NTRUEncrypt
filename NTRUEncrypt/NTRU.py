from sage.all import *
import random

class NTRU:
    
    def __init__(self, level):
        if level == 0:
            self.N = 11
            self.q = 32
            self.p = 3
        elif level == 1:
            self.N = 167
            self.q = 128
            self.p = 3
            self.df = 30
            self.dg = 23
        elif level == 2:
            self.N = 251
            self.q = 128
            self.p = 3
        elif level == 3:
            self.N = 347
            self.q = 128
            self.p = 3
        elif level == 4:
            self.N = 401
            self.q = 2048
            self.p = 3
            self.d1 = 8
            self.d2 = 8
            self.d3 = 6
            self.dg = 133
            self.dm = 101
        elif level == 5:
            self.N = 439
            self.q = 2048
            self.p = 3
            self.d1 = 9
            self.d2 = 8
            self.d3 = 5
            self.dg = 156
            self.dm = 112
        elif level == 6:
            self.N = 593
            self.q = 2048
            self.p = 3
            self.d1 = 10
            self.d2 = 10
            self.d3 = 8
            self.dg = 197
            self.dm = 158
        elif level == 5:
            self.N = 439
            self.q = 2048
            self.p = 3
            self.d1 = 11
            self.d2 = 11
            self.d3 = 15
            self.dg = 147
            self.dm = 204
        else:
            self.N = 503
            self.q = 256
            self.p = 3
            self.df = 60
            self.dg = 30
        
    def generate_random_pol(self, lower, upper, N):
        coefs = []
        for i in range(N):
            coefs.append(int(random() * (upper - lower + 1)) + lower)
        return self.R(coefs)
    
    def generate_random(self, lower, upper):
        lower_array = [-1] * lower
        upper_array = [1] * upper
        zero_array = [0] * (self.N - (lower + upper))
        poly = lower_array + upper_array + zero_array
        random.shuffle(poly)
        return self.R(poly)
        
    
    def create_keys(self):
        self.R = PolynomialRing(QQ, 'x')
        x = self.R.gen()
        gcd = 0
        while gcd != 1:
            self.f = self.generate_random(self.df - 1, self.df)
            print(self.f)
            self.g = self.generate_random(self.dg, self.dg)
            print(self.g)
            extended_gcd = xgcd(x**self.N -1, self.f)
            gcd = extended_gcd[0]
            u = extended_gcd[1]
            v = extended_gcd[2]
            print(gcd)
        self.fp = self.mod(v, self.p)
        self.fq = self.mod(v, self.q)
        self.h = self.recenter(self.mul(self.p * self.fq, self.g),self.q)
        
    def new_create_keys(self):
        self.R = PolynomialRing(QQ, 'x')
        x = self.R.gen()
        gcd = 0
        while gcd != 1:
            self.f1 = self.generate_random(0, self.d1)
            self.f2 = self.generate_random(0, self.d2)
            self.f3 = self.generate_random(0, self.d3)
            self.f = 1 + (2 * (self.f1 * self.f2 + self.f3))
            self.f = self.f % (x**self.N - 1)
            print(self.f)
            self.g = self.generate_random(self.dg, self.dg)
            print(self.g)
            extended_gcd = xgcd(x**self.N -1, self.f)
            gcd = extended_gcd[0]
            u = extended_gcd[1]
            v = extended_gcd[2]
        self.fp = self.mod(v, self.p)
        self.fq = self.mod(v, self.q)
        self.h = self.recenter(self.mul(self.p * self.fq, self.g), self.q)
        
        
    def test(self):
        self.R = PolynomialRing(ZZ, 'x')
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
        random_pol = self.generate_random(10,10)
        #random_pol = -1 + x**2 + x**3 + x**4 - x**5 - x**7
        message_poly = self.mapping(self.encode(message))
        #message_poly = -1 + x**3 - x**4 - x**8 + x**9 + x**10
        print("message_poly")
        print(message_poly)
        temp = self.mul(h, random_pol)
        secret = self.mod(temp + message_poly, self.q)
        return secret
    
    def new_cipher(self, message, h):
        x = self.R.gen()
        random_pol = self.generate_random(10,10)
        message_poly = self.mapping(self.encode(message))
        secret = h * random_pol
        secret = secret % (x**self.N - 1)
        secret = self.mod(secret + message_poly, self.q)
        return secret
    
    def new_decipher(self, secret):
        x = self.R.gen()
        a = self.recenter((secret * self.f) % (x ** self.N - 1), self.q)
        b = self.recenter(a, self.p)
        c = self.recenter((self.fp * b) % (x ** self.N - 1), self.p)
        message = self.decode(self.inverse_mapping(self.group(c.list())))
        return message

    def decipher(self, secret):
        print(secret)
        a = self.recenter(self.mul(secret, self.f), self.q)
        print(a)
        b = self.recenter(a, self.p)
        print(b)
        c = self.mul(self.fp, b)
        print(c)
        c = self.recenter(c, self.p)
        message = self.decode(self.inverse_mapping(self.group(c.list())))
        return message
        
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
    
    def mul(self, poly_a, poly_b):
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
    
    def decode(self, grouped_list):
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
        for i in range(0, len(list), 2):
            co_list.append([list[i], list[i + 1]])
        return co_list
        
    
    # def decipher(message):
