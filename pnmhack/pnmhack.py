# A pnmhack object represents a PNM file _on the disk_.

import subprocess
import os
import os.path as path

class pnmhack():
    def __init__(self, filename, handle=None):
        # d: directory; fn: base filename without suffix; suf: suffix, without dot
        if handle is None:
            self.fh = open(filename, "r")
        else:
            self.fh = handle
        self.set_filename(filename)
        self.seq = 1;
        self.reset()

    def set_filename(self, filename):
        self.filename = filename
        (self.d, fn) = path.split(filename)
        (self.fn, self.suf) = str.split(fn, '.', 1)

    # pull the file pointer back to the beginning of the file
    def reset(self):
        self.fh.seek(0, 0)

    def genfilename(self):
        seq = self.seq
        self.seq += 1
        return path.join(self.d, 
                         "%s%04d.%s" % (self.fn, seq, self.suf))

    def rename(self, newname):
        os.rename(self.filename, newname)
        self.set_filename(newname)

    def filter(self, command, outputfile=None):
        if outputfile is None:
            outputfile = self.genfilename()
        self.reset()
        ofh = open(outputfile, "w+")
        subprocess.run(command, stdin=self.fh, stdout=ofh)
        ofh.writable = False
        return self.__class__(outputfile, ofh)

    def copy(self):
        return self.filter(["cat"])

    def scale(self, xsize=None, ysize=None):
        opt = None
        if xsize is None:
            if ysize is None: pass
            else:             opt = ['-ysize', ysize]
        else:
            if ysize is None: opt = ['-xsize', xsize]
            else:             opt = ['-xysize', xsize, ysize]
        if opt is None:
            raise Exception("scale() missing at least one of xsize, ysize")
        
        return self.filter(["pnmscale", *opt])
    
def ok(a, x, msg):
    if (a == x): print("ok", msg)
    else:
        print("not ok", msg)
        print("# actual:  ", str(a))
        print("# expected:", str(x))
                
if __name__ == '__main__':
    devnull = open("/dev/null")

    # These are unit tests
    p = pnmhack("/tmp/foo.pnm", handle=devnull)
    ok(p.d, "/tmp", "directory")
    ok(p.fn, "foo", "basename")
    ok(p.suf, "pnm", "suffix")
    ok(p.seq, 1, "sequence number")

    ok(p.genfilename(), "/tmp/foo0001.pnm", "genfilename 1")
    ok(p.genfilename(), "/tmp/foo0002.pnm", "genfilename 2")
