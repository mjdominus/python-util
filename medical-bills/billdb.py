
# import html.parser
import xml.etree.ElementTree as ET

class billdb():
    def __init__(self, file, rdonly=False,
                 debug=False):
        self.rdonly = rdonly
        self.path = file
        self.debug = debug
        self.parser = ET
        self.tree = None
        self.db = {}
        self.openfile()

    def openfile(self):
        if self.path is None: self.fail("omitted file argument")
        mode = 'r+'
        if self.rdonly: mode = 'r'
        self.f = open(self.path, mode=mode)
        self.loadfile()

    def loadfile(self):
        self.tree = self.parser.parse(self.f)
        for row in self.root():
            self.addrow(row)
        if self.debug:
            print("Loaded", len(self.db), "row(s)")

    def skippable_row(self, row):
        # we expect there to be a row of TH cells
        # at the top of the input
        if row.tag.lower() == 'tr':
            for child in row:
                if child.tag.lower() != 'th':
                    return False
            return True
        else:
            return False
        
    # row is an Element object, should be
    # a TR element containing TD subelements
    def addrow(self, row):
        if self.skippable_row(row): return
        if row.tag.lower() != 'tr':
            raise Exception("Row had tag '" + row.tag +
                            "' instead of expected TR");
        
        claim_number = self.unpack_td(row[0])
        rec = { "claim_number": claim_number }

        rec["date"]         = self.unpack_td(row[1])
        rec["for"]          = self.unpack_td(row[2])
        rec["type"]         = self.unpack_td(row[3])
        rec["doctor"]       = self.unpack_td(row[4])
        rec["total"]        = self.unpack_td(row[5])
        rec["payable"]      = self.unpack_td(row[6])
        rec["status"]       = self.unpack_td(row[7])

        rec["mystatus"]     = None
        rec["date_paid"]    = None
        rec["check_number"] = None
        rec["check_amount"] = None

        if self.db.get(claim_number) is not None:
            self.merge_record(claim_number, rec)
            return
        else:
            self.db[claim_number] = rec

    def get_claim(self, claim_number):
        self.db.get(claim_number)

    def has_claim(self, claim_number):
        return claim_number in self.db

    # Here we are presented with a new record
    # that has the same ID as an old record
    def merge_record(self, id, rec):
        raise Exception("Duplicate record: claim number " +
                        id);
        
        
    def unpack_td(self, elem):
        s = str(ET.tostring(elem))
        text = self.alltext(elem)
        if elem.tag != 'TD':
            raise Exception("element '" + s + "' has tag '" + elem.tag + "' instead of TD")
        elif text is None:
            raise Exception("element '" + s + "' has no text")
        return text
        
    def fail(self, msg):
        raise Exception("billdb: " + msg)

    def root(self):
        return self.tree.getroot()

    def alltext(self, elem):
        return "".join(elem.itertext())

if __name__ == '__main__':
    bdb = billdb("samples/a.xls", debug=True)
    from pprint import pprint as pp
    pp(vars(bdb))
