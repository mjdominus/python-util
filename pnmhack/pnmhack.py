# A pnmhack object represents a PNM file _on the disk_.

import subprocess
import os
import os.path as path
import re

class pnmhack():
    def __init__(self, filename, handle=None, persist=True):
        # d: directory; fn: base filename without suffix; suf: suffix, without dot
        if handle is None:
            self.fh = open(filename, "r")
        else:
            self.fh = handle
        self.set_filename(filename)
        self.seq = 1;
        self.persistent = persist
        self.reset()

    def dummy():
        pnmhack("/dev/null")

    def __del__(self):
        if not self.persistent:
            print("Cleaning up %s" % self.filename)
            os.remove(self.filename)

    def pad_list(ls, ln, pad=None):
        ls += [pad] * (ln - len(ls))
        return ls
            
    def set_filename(self, filename):
        self.filename = filename
        (self.d, fn) = path.split(filename)
        (self.fn, self.suf) = pad_list(str.split(fn, '.', 1), 2, "")

    # pull the file pointer back to the beginning of the file
    def reset(self):
        self.fh.seek(0, 0)

    def fresh_file(self):
        seq = self.seq
        self.seq += 1
        while True:
            newname = path.join(self.d, 
                                "%s%04d.%s" % (self.fn, seq, self.suf))
            try:
                fd = os.open(newname, os.O_RDWR | os.O_EXCL | os.O_CREAT, 0o666)
                return os.fdopen(fd)
            except FileExistsError:
                self.seq += 1

    def rename(self, newname):
        os.rename(self.filename, newname)
        self.set_filename(newname)

    def filter(self, command, outputfile=None):
        if outputfile is None:
            ofh = self.fresh_file()
        else:
            ofh = open(outputfile, "w+")
        self.reset()
        subprocess.run(command, stdin=self.fh, stdout=ofh)
        ofh.writable = False
        return self.__class__(outputfile, ofh, persist=False)

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

    def cut(self, **kwargs):
        opts = []
        xopts = 0
        for xopt in [ "left", "right", "width" ]:
            if xopt in kwargs:
                opts += [ "-" + xopt, str(kwargs[xopt]) ]
                xopts += 1
        yopts = 0
        for yopt in [ "top", "bottom", "height" ]:
            if yopt in kwargs:
                opts += [ "--" + yopt, str(kwargs[yopt]) ]
                yopts += 1
        if xopts > 2:
            raise Exception("cut() may not have all of left, right, width");
        if yopts > 2:
            raise Exception("cut() may not have all of top, bottom, height");
        return self.filter(["pnmcut", *opts])

    def operate(self, command, stdout=subprocess.PIPE):
        result = subprocess.run(command,
                                stdin=self.fh, stdout=stdout)
        if result.stdout is not None:
            return result.stdout.decode()
        else:
            return None
    
    def size(self):
        # B.pnm:	PPM raw, 1536 by 2048  maxval 255
        result = self.operate(["pnmfile", "-"]);
        match = re.search(r'(\d+) by (\d+)', result)
        if match is None:
            raise Error("Couldn't parse output of pnmfile\n\t<%s>\n"
                        % result)
        return [ int(x) for x in match.groups() ]

    def _resolve_method(self, name):
        try:
            return self.__getattribute__(method_name)
        except AttributeError:
            return None

    def export_as(self, format, filename=None):
        method = self._resolve_method("export_as_" + format)
        if method is None:
            raise Exception("Don't know how to export in format '%s'" % format)
        if filename is None:
            filename = path.join(self.d, "%s.%s" % (self.fn, format))
        return method.__call__(filename)
    
    def export_as_jpeg(self, filename):
        print("exporting %s as jpeg %s ..." % (self.filename, filename))
        outfile = open(filename, "w")
        self.operate(["cjpeg"], stdout=outfile)

    # Guess the format
    def import_smartly(self, filename):
        # If the filename has a recognized suffix, use that
        if re.search(r'\.', filename):
            parts = str.split(filename, '.')
            suffix = parts[-1]
            method = self._resolve_method("import_from_" + format)
            if method is not None:
                return method.__call__(filename)

        # Otherwise try running file(1) or something
        raise Exception("Can't import file %s" % filename)

    def import_from(self, format, filename):
        method = self._resolve_method("import_from_" + format)
        if method is None:
            raise Exception("Don't know how to export in format '%s'" % format)
        return method.__call__(filename)

    def import_from_jpeg(self, filename):
        return self.filter(["djpeg", filename])
    
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
