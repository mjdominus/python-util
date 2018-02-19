#!/usr/bin/python3

from billdb.__root_package import billdb

if __name__ == '__main__':
    bdb = billdb("samples/arec.bdb", debug=True) \
        .import_xml("samples/a.xls").save()


