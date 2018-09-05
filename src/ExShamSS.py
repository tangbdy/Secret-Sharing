# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 08:27:31 2018

@author: Tang
"""

import random
#import math
import miller_rabin
from ExEuclid import findModReverse as rev

#default params
n = 50
t = 30
k = 16
x = []      #n
#polynomial coefficient  k * t
a = []
# shadow secret  n * k
f = [] 
d = []      #k
w = []      #k
Crfi = []       #j

#set fi && every element minus 1 && length 16
#setfi = [0, 1, 2, 3, 4, 5, 8, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 24, 26]
setfi = range(t)

def encode(s):
    c_list = []
    for c in s:
        c_1 = bin(ord(c)).replace('0b', '')
        c_1 = '0' * (7 - len(c_1)) + c_1
        c_list.append(c_1)
    return ' '.join(c_list)
    
def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


# 1)initation
def Myinit(n, x, p):
    for r in range(n):
        x.append(random.randint(1, p-1))

# 2)secret distribution
#   Step 1
def polyset(t, a, p):
    global k
    for l in range(k):
        a.append([])
        for m in range(t):
            atemp = random.randint(1, p - 1)
            a[l].append(atemp)

def func(l, x):
    y = 0
    for m in range(len(a[l])):
        y += (a[l][m] * pow(x, m))
    return y % p

#   Step 2
def shadow(a, x, f):
    global k
    y = 0
    for r in range(n):
        f.append([])
        for l in range(k):
            for m in range(t):
                y += (a[l][m] * pow(x[r], m))
                f[r].append(y % p)

#   Step 3 and 4
def setdw(k, p, x):
    sumfunc = 0

    while(len(w) < k):
        wtemp = random.randint(1, p-1)
        if (wtemp not in x) and (wtemp not in w):
            w.append(wtemp)

    for i in range(k-1):
        d.append(random.randint(1, p-1))

    for l in range(k-1):
        sumfunc += d[l] * func(l, w[l])

    d.append(((s - sumfunc) * rev(func(k - 1, w[k - 1]), p)) % p)
    
# 3) secret recovery
def calCrfi(k, x, d, w, p):
    # setfi is chosen by key distributor D
    j = len(setfi)
    for r in range(j):
        ctemp = 0
        for l in range(k):
            pai = 1
            for v in range(j):
                if v != r:
                    pai *= (w[l] - x[setfi[v]]) * rev((x[setfi[r]] - x[setfi[v]]) % p, p)
            ctemp += d[l] * func(l, x[setfi[r]]) * (pai % p)
        Crfi.append(ctemp % p)
    
if __name__ == '__main__':
    p = miller_rabin.prime_generate(310)
  
    secret_str = input('please input your secret\n')
    secret_bin = ''.join(encode(secret_str).split())
    s = int(secret_bin, 2)
    
    Myinit(n, x, p)
    polyset(t, a, p)
    shadow(a, x, f)
    setdw(k, p, x)
    
    calCrfi(k, x, d, w, p)
    
    s_1 = sum(Crfi) % p


    s_2 = bin(s_1).replace('0b', '')
    s_2 = '0' * (len(secret_bin) - len(s_2)) + s_2
    s_3 = list(s_2)
    
    jcount, kcount = 0, 1
    while (7 * kcount + jcount < len(encode(secret_str))):
        jcount += 1
        kcount += 1
    
    for jlit, klit in zip(range(jcount), range(1, kcount)):
        s_3.insert(7 * klit + jlit, ' ')
    
    s_4 = ''.join(s_3)
    s_recovered =decode(s_4) 
    
    print('your original secret is:', s_recovered)







