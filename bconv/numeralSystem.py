#!/usr/bin/python3

class numeralSystem():
    __knownDigitStyle = { 'letterDigits' : 1, 'decimalDigits' : 1 }

    def __init__(self, base, sep="", digitStyle=None):
        self.base = int(base)
        if digitStyle is None:
            if base > 36: digitStyle = 'decimalDigits'
            else: digitStyle = 'letterDigits'
            
        try:
            self.__knownDigitStyle[digitStyle]
            self.digitStyle = digitStyle
        except KeyError:
            raise KeyError("Unknown digitStyle '%s'" % digitStyle);

        if self.digitStyle == "letterDigits" and base > 36:
            raise Exception("'letterDigits' style only makes sense for base 36 or less");

        self.sep = sep

    def interpret(self, s):
        """given a string s that contains a numeral,
        return the number that it represents"""
        if self.base == 10: return int(s)
        res = 0
        for digit in self.digits(s):
            res = res * self.base + self.digit_value(digit)
        return res

    def represent(self, n):
        """given a number n, produce its numeral representation"""
        if self.base == 10: return str(n)
        out = []
        while n > 0:
            out = [self.output_digit(n % self.base)] + out
            n = int(n / self.base)
        if len(out) == 0: out = ["0"]
        return self.sep.join(out)

    def digits(self, s):
        """given a numeral s, split it into a list of digits 
        and return the list"""
        if self.sep is None:
            return list(s)
        else:
            return s.split(self.sep)

    def digit_value(self, d):
        """d is a string containing a 'digit' in this system
        digit_value() returns the numeric value of this digit"""
        if self.digitStyle == "decimalDigits": return int(d)
        elif self.digitStyle == "letterDigits":
            if d.isdigit():
                return int(d)   # no range checking yet

            val = ord(d);
            if val >= ord('A') and val <= ord('Z'):
                return val - ord('A') + 10
            elif val >= ord('a') and val <= ord('z'):
                return val - ord('a') + 10
            raise Exception("Unrecognized digit '%s' (#%d)" %
                            (d, val))
        else: raise Exception("Unknown digitStyle '%s'" % self.digitStyle)
            

    def output_digit(self, n):
        """n is a number that should be represented with a single
        output digit.  Return the string for that digit."""
        if self.digitStyle == "decimalDigits":
            return "%02d" % n
        elif self.digitStyle == "letterDigits":
            if n <= 9: return str(n)
            elif n <= 36: return (n - 10 + ord("a")) # no uppercase option yet
            else:
                raise Exception("Can't generate digit for value %d" % n)
        else: raise Exception("Unknown digitStyle '%s'" % self.digitStyle)
            
            

        
