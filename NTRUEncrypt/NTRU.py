import sys
from sage.all import *


class NTRU:
    
    def __init__(self):
        self.N = 503
        self.q = 256
        self.p = 3
    
    def encode(message):
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
    
    def mapping(bits_list):
        co_list = []
        for bits in bits_list:
            if bits == [0, 0, 0]:
                co_list.append([0, 0])
            elif bits == [0, 0, 1]:
                co_list.append([0, 1])
            elif bits == [0, 1, 0]:
                co_list.append([0, -1])
            elif bits == [0, 1, 1]:
                co_list.append([1, 0])
            elif bits == [1, 0, 0]:
                co_list.append([1, 1])
            elif bits == [1, 0, 1]:
                co_list.append([1, -1])
            elif bits == [1, 1, 0]:
                co_list.append([-1, 0])
            elif bits == [1, 1, 1]:
                co_list.append([-1, 1])
        return co_list
    
    def inverse_mapping(co_list):
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
    
    # def decipher(message):