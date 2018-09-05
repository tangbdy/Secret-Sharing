# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:36:01 2018

@author: tanglt
"""
from random import randint
import math

prime_10000 = []
for line in open('prime_10000.txt'):
    theline = line.split()
    for x in range(len(theline)):
        prime_10000.append(int(theline[x]))
        
def xn_mod_p(x, n, p):
    if n == 0:
        return 1
    res = xn_mod_p((x*x)%p, n>>1, p)
    if n&1 != 0:
        res = (res*x)%p
    return res

def xn_mod_p2(x, n, p):
    res = 1
    n_bin = bin(n)[2:]
    for i in range(0, len(n_bin)):
        res = res**2 % p
        if n_bin[i] == '1':
            res = res * x % p
    return res

def simple_prime_test(p):
    if p < 10000:
        print ('The value typed in must be bigger than 10000')
        raise ValueError
    for x in prime_10000:
        if p % x == 0:
            return False
    return True

def miller_rabin_witness(a, p):
    if p == 1:
        return False
    if p == 2:
        return True
    #p-1 = u*2^t 求解 u, t
    n = p - 1
    t = int(math.floor(math.log(n, 2)))
    u = 1
    while t > 0:
        u = n // 2**t
        if n % 2**t == 0 and u % 2 == 1:
            break
        t = t - 1

    b1 = b2 = xn_mod_p2(a, u, p)
    for i in range(1, t + 1):
        b2 = b1**2 % p
        if b2 == 1 and b1 != 1 and b1 != (p - 1):
            return False
        b1 = b2
    if b1 != 1:
        return False
    return True
def prime_test_miller_rabin(p, k):
    while k > 0:
        a = randint(1, p - 1)
        if not miller_rabin_witness(a, p):
            return False
        k = k - 1
    return True

#生成n位素数
def prime_generate(n):
    randnum = randint(10**(n-1),10**n-1)
    if randnum % 2 == 0:
        randnum = randnum + 1
    while simple_prime_test(randnum) == False:
        randnum = randnum + 2
    #Miller-Rabin测试10次
    while prime_test_miller_rabin(randnum, 10) == False:
        randnum = randnum + 2
    if randnum > 10**n-1:
        return prime_generate(n)
    else:
        return randnum
        
    
    