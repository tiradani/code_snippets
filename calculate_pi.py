#!/usr/bin/python
"""
Original Code Source:   http://blog.recursiveprocess.com/2013/03/14/calculate-pi-with-python/
Modified by:            Anthony Tiradani
Date:                   10/17/2016
"""
import sys
import time
import traceback

from decimal import *
from fork import ForkManager

def factorial(n):
    if n < 1:
        return 1
    else:
        return n * factorial(n-1)

class CalculatePI(object):
    def __init__(self): pass

    def plouffBig(self, n):
        # http://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
        pi = Decimal(0)
        k = 0
        while k < n:
            pi += (Decimal(1)/(16**k))*((Decimal(4)/(8*k+1))-(Decimal(2)/(8*k+4))-(Decimal(1)/(8*k+5))-(Decimal(1)/(8*k+6)))
            k += 1
        return pi

    def bellardBig(self, n):
        # http://en.wikipedia.org/wiki/Bellard%27s_formula
        pi = Decimal(0)
        k = 0
        while k < n:
            pi += (Decimal(-1)**k/(1024**k))*(Decimal(256)/(10*k+1)+Decimal(1)/(10*k+9)-Decimal(64)/(10*k+3)-Decimal(32)/(4*k+1)-Decimal(4)/(10*k+5)-Decimal(4)/(10*k+7)-Decimal(1)/(4*k+3))
            k += 1
        pi = pi * 1/(2**6)
        return pi

    def chudnovskyBig(self, n): #http://en.wikipedia.org/wiki/Chudnovsky_algorithm
        pi = Decimal(0)
        k = 0
        while k < n:
            pi += (Decimal(-1)**k)*(Decimal(factorial(6*k))/((factorial(k)**3)*(factorial(3*k)))* (13591409+545140134*k)/(640320**(3*k)))
            k += 1
        pi = pi * Decimal(10005).sqrt()/4270934400
        pi = pi**(-1)
        return pi

def do_calculation(precision):
    output = ""
    try:
        total_size = precision + 2
        getcontext().prec = precision

        calculator = CalculatePI()
        header_format = "{:<20} {:{align}{width}} {:{align}{width}} {:{align}{width}}\n"
        output += header_format.format(' ', 'Plouff', 'Bellard', 'Chudnovsky', align='<', width=total_size)
        data_format = "{:<16} {:<2}  {:{align}{width}} {:{align}{width}} {:{align}{width}}\n"
        for i in xrange(1,20):
            plouff = calculator.plouffBig(i)
            bellard = calculator.bellardBig(i)
            chudnovsky = calculator.chudnovskyBig(i)
            output += data_format.format("Iteration number", i, plouff, bellard, chudnovsky, align='<', width=total_size)
    except:
        output = traceback.format_exc()

    return output

def main(args):
    # Sets decimal to 25 digits of precision
    precision = 25
    number_of_forks = 2000
    if len(args) > 1: precision = int(args[1])
    if len(args) > 2: number_of_forks = int(args[2])

    fork_manager = ForkManager()
    fork_manager.add_fork("do_calculation", do_calculation, precision)
    results = fork_manager.bounded_fork_and_collect(number_of_forks, sleep_time=0.01)
    for item in results:
        print results[item]

if __name__ == "__main__":
    sys.exit(main(sys.argv))
