#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for C++ module xxd.morton.
"""

from random import getrandbits
import sys
sys.path.insert(0,'.')

import numpy as np

import xxd.morton


u10 = [1/2]
while len(u10) < 10:
    u = u10[-1]/2
    u10.append(u)
u10 = np.array(u10, dtype=np.single)

def binstr2f(binstr, verbose=False):
    """Compute the dot product of binstr and u10. 
    
    :param str binstr: a str of 1s and 0s of length <= 10. Padded with zeros until length is 10.
    
    :raises RuntimeError: if binstr is not compliant.
    :return: dot product of binstr and u10
    :rtype: np.single
    """
    if not isinstance(binstr,str):
        raise RuntimeError('binstr2intc expects a str argument')
    if len(binstr)>10:
        raise RuntimeError('str argument must not be longer than 10 characters')
    for c in binstr:
        if not c in '10':
            raise RuntimeError('str argument must contain only 1 or 0.')
    # Pad with zero until length 10
    while len(binstr)<10:
        binstr += '0'
    
    f = np.single(0)
    for i in range(10):
        if binstr[i] == '1':
            f += u10[i]
    if verbose:
        print(f"{binstr} -> {f} ({type(f)})")
    return f


def random_binstr():
    """return a random bit str of length 10."""
    s = ''
    for i in range(10):
        b = getrandbits(1)
        s += '1' if b else '0'
    return s

    
def dilate(binstr,coord):
    dilated = ''
    if coord == 'x':
        for b in binstr:
            dilated += b+'  '
    elif coord == 'y':
        for b in binstr:
            dilated += ' '+b+' '
    elif coord == 'z':
        for b in binstr:
            dilated += '  '+b
    else:
        raise RuntimeError('bad coord argument.')
    return dilated
    
def dilate3(x,y,z):
    s = ''
    for i in range(10):
        s += x[i]+y[i]+z[i]
    return s
    
def test_cpp_morton_code_1():
    
    for count in range(1000000):
        # generate three bit strings of length 10
        bx = random_binstr()
        by = random_binstr()
        bz = random_binstr()
        morton_code(bx,by,bz)
        

def morton_code(bx,by,bz):
    # find their corresponding np.float value
    x = binstr2f(bx)
    y = binstr2f(by)
    z = binstr2f(bz)        
    print(f"x {bx} {x:14} {dilate(bx,'x')}")
    print(f"y {by} {y:14} {dilate(by,'y')}")
    print(f"z {bz} {z:14} {dilate(bz,'z')}")
    # interleave the bit strings into a Morton code
    s3 = dilate3(bx,by,bz)
    print(f"{' '*27} {s3}")
    # compute the morton code for (x,y,z)
    m = str(bin(xxd.morton.code1(x,y,z)))[2:]
    while len(m) < 30:
        m = '0' + m
    print(f"{'morton.code1(x,y,z)':>27} {m}")
    print()
    # test:
    assert m == s3


def test_cpp_morton_code_2():
    bx = '0000000001'
    morton_code(bx,bx,bx)
    for i in range(9):
        bx = bx[1:]+'0'
        morton_code(bx,bx,bx)
    

def test_cpp_morton_code_3():
    bx = '0000000001'
    bz = by = '0000000000'
    morton_code(bx,by,bz)
    for i in range(9):
        bx = bx[1:]+'0'
        morton_code(bx,by,bz)
    

#===============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
#===============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_cpp_morton_code_1

    print(f"__main__ running {the_test_you_want_to_debug} ...")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
#===============================================================================
