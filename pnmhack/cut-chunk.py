#!/usr/bin/python3

import argparse
from pnmhack import pnmhack

class cut_chunk():
    def __init__(self):
        self.argparser().parse_args(namespace=self)

    def argparser(self):
        p = argparse.ArgumentParser(prog="cut-chunk")
        p.add_argument('--aspect', required=True, type=pnmhack)
        p.add_argument('--scale', action='store_true')
        p.add_argument('--offset', default=0, type=int)
        p.add_argument('source', type=pnmhack)
        return p

    def go(self):
        z = import_from_jpeg
        (sw, sh) = self.source.size()
        (aw, ah) = self.aspect.size()
        ar = aw / ah
        th = sh
        tw = th * ar
        # XXX what if tw > sw?
        piece = self.source.cut(left=self.offset, width=tw)
        piece.export_as("jpeg")
                                
        

from pprint import pprint
        
if __name__ == '__main__':
#    app = cut_chunk()
    dummy = pnmhack.dummy()
    #
#    app.source.cut(width=100, height=200).export_as("jpeg")
#    app.go()
    
