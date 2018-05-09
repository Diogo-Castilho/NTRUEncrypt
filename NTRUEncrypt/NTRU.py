from sage.all import *
import random
import os
from hashlib import sha256


class NTRU:
    
    def __init__(self, level):
        self.q = 2048
        self.p = 3
        if level == 0:
            self.N = 401
            self.d1 = 8
            self.d2 = 8
            self.d3 = 6
            self.dg = 133
            self.dm = 101
        elif level == 1:
            self.N = 439
            self.d1 = 9
            self.d2 = 8
            self.d3 = 5
            self.dg = 146
            self.dm = 112
        elif level == 2:
            self.N = 593
            self.d1 = 10
            self.d2 = 10
            self.d3 = 8
            self.dg = 197
            self.dm = 158
        elif level == 3:
            self.N = 743
            self.d1 = 11
            self.d2 = 11
            self.d3 = 15
            self.dg = 247
            self.dm = 204
        
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
    
    def generate_random_n(self, lower, upper, n):
        lower_array = [-1] * lower
        upper_array = [1] * upper
        zero_array = [0] * (n - (lower + upper))
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
        self.fp = self.mod(v, self.p)
        self.fq = self.mod(v, self.q)
        self.h = self.recenter(self.mul(self.p * self.fq, self.g),self.q)
        
    def new_create_keys(self):
        self.R = PolynomialRing(QQ, 'x')
        x = self.R.gen()
        gcd = 0
        while gcd != 1:
            self.f1 = self.generate_random(self.d1, self.d1)
            self.f2 = self.generate_random(self.d2, self.d2)
            self.f3 = self.generate_random(self.d3, self.d3)
            self.f = 1 + ((3)* (((self.f1 * self.f2) % (x**self.N - 1)) + self.f3))
            self.g = self.generate_random(self.dg, self.dg + 1)
            extended_gcd = xgcd(x**self.N -1, self.f)
            gcd = extended_gcd[0]
            v = extended_gcd[2]
        self.fp = self.mod(v, self.p)
        self.fq = self.mod(v, self.q)
        self.h = self.recenter((self.p * self.fq * self.g) % (x**self.N - 1), self.q)
    
    def mgf(self, r_string, iterations):
        counter = 0
        hash = r_string
        while counter < iterations:
            hash = sha256(hash.encode('ascii')).hexdigest()
            counter += 1
        counter = 0
        poly_coefs = []
        while counter < self.N:
            poly_coefs.append(ord(hash[counter % len(hash)]))
            counter += 1
        print(poly_coefs)
        return self.R(poly_coefs)
        
        
    
    def cipher(self, message, h):
        x = self.R.gen()
        b = self.generate_random(self.dm, self.dm)
        m = self.mapping(self.encode(message))
        m_prime =  (m * b) % (x**self.N - 1)
        r_prime = ((m_prime * b) % (x**self.N - 1)) + h
        r = ((self.p * r_prime) * h) % (x**self.N - 1)
        r_list = r.list()
        r_list.append(0)
        print(len(r_list))
        r_string = self.decode(self.inverse_mapping(self.group(r_list)))
        mask = self.mgf(r_string, 20)
        m = self.mod(m_prime + mask, self.p)
        #secret = self.mod(r + m, self.q)
        secret = self.mod(r + m, self.q)
        return secret
    
    
    
    
    def decipher(self, secret):
        m = self.mod(secret * self.f, self.p)
        r = secret - m
        r_list = r.list()
        r_list.append(0)
        r_string = self.decode(self.inverse_mapping(self.group(r_list)))
        mask = self.mgf(r_string, 20)
        m_prime = m - mask
        
        
    
    
    def new_cipher(self, message, h):
        x = self.R.gen()
        random_pol = self.generate_random(self.dm - 1, self.dm)
        message_poly = self.mapping(self.encode(message))
        secret = h * random_pol
        secret = secret % (x**self.N - 1)
        secret = self.mod(secret + message_poly, self.q)
        return secret
    
    def count(self, message, number):
        counter = 0
        m_list = message.list()
        for i in range(len(m_list)):
            if number == m_list[i]:
                counter += 1
                print("here")
        return counter
    
    def new_decipher(self, secret):
        x = self.R.gen()
        a = self.recenter((secret * self.f) % (x ** self.N - 1), self.q)
        b = self.recenter(a, self.p)
        #c = self.recenter((self.fp * b) % (x ** self.N - 1), self.p)
        message = self.decode(self.inverse_mapping(self.group(b.list())))
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
    
    def encode(self, message):
        bit_list = []
        for char in message:
            bits = bin(ord(char))[2:]
            bits = '00000000'[len(bits):] + bits
            bit_list.extend([int(bit) for bit in bits])
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
    
    def group(self, ungrouped):
        co_list = []
        for i in range(0, len(ungrouped), 2):
            co_list.append([ungrouped[i], ungrouped[i + 1]])
        return co_list
