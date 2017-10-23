#!/usr/bin/python3

from sys import (argv, stderr)
import fileinput

def interpret(s, ibase):
    """given a string n that contains a base-ibase numeral,
    return the number that it represents"""
    if ibase == 10: return int(s)
    res = 0
    for digit in list(s):
       res = res * ibase + digit_value(digit)
    return res
    
def represent(n, obase):
    """given a number n, produce its base-obase representation"""
    if obase == 10: return str(n)
    out = ""
    while n > 0:
        out = output_digit(n % obase) + out
        n = int(n / obase)
    if out == "": out = "0"
    return out

def bconv(s, ibase, obase):
    return represent(interpret(s, ibase), obase)

def digit_value(digit):
    """numeric value of the given 'digit'"""
    if digit.isdigit():         # also handles weird Unicode digits
        return int(digit)
    else:
        val = ord(digit);
        if val >= ord('A') and val <= ord('Z'):
            return val - ord('A') + 10
        elif val >= ord('a') and val <= ord('z'):
            return val - ord('a') + 10
        else:
            raise Exception("Unrecognized digit '%s' (#%d)" %
                            (digit, val))

def output_digit(n):
    """output representation for a single 'digit' with value n"""
    if n <= 9: return str(n)
    elif n <= 36: return chr(n - 10 + ord("a"))
    else:
        raise Exception("Can't generate digit for value %d" % n)

def usage():
    print('Usage: %s input-base [output-base]\n\toutput-base defaults to 10' % argv[0],
          file=stderr)
    exit(2)
    
def main():
    obase = 10
    if (len(argv) == 2): ibase = int(argv[1])
    elif (len(argv) == 3): ibase = int(argv[1]); obase = int(argv[2])
    else: usage()
    del argv[1:]

    for line in fileinput.input():
        print(bconv(line.rstrip(), ibase, obase))

if __name__ == "__main__":
    main();

