#!/usr/bin/python3

from sys import (argv, stderr)
import fileinput
from numeralSystem import numeralSystem

class bConv():
    def __init__(self, ibase, obase, istyle=None, ostyle=None,
                 isep=None, osep=None):
        self.iconv = numeralSystem(ibase, sep=isep, digitStyle=istyle);
        self.oconv = numeralSystem(obase, sep=osep, digitStyle=ostyle);
        
    def convert(self, s):
        return self.oconv.represent(self.iconv.interpret(s))

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

    kwargs = {}
    if ibase > 36: kwargs["isep"] = ".";  kwargs["istyle"] = "decimalDigits"
    else:          kwargs["isep"] = None; kwargs["istyle"] = "letterDigits"
    if obase > 36: kwargs["osep"] = ".";  kwargs["ostyle"] = "decimalDigits"
    else:          kwargs["osep"] = "";   kwargs["ostyle"] = "letterDigits"

    converter = bConv(ibase, obase, **kwargs)
    
    for line in fileinput.input():
        print(converter.convert(line.rstrip()))

if __name__ == "__main__":
    main();

