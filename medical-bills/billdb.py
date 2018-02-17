#!/usr/bin/python3

# import html.parser
import xml.etree.ElementTree as ET
import yaml
import os

class billdb():
    def __init__(self, path, rdonly=False, debug=False, tmpfile=None, backupfile=None):
        self.debug = debug
        self.rdonly = rdonly
        self.path = path
        if tmpfile is None:
            self.tmpfile = path + ".tmp"
        else:
            self.tmpfile = tmpfile
        if backupfile is None:
            self.backupfile = path + ".bkp"
        else:
            self.backupfile = backupfile
        self.open_file(self.path)
        self.parser = ET
        self.db = {}
        self.load()

    def mode(self):
        if self.rdonly: return "r"
        else: return "r+"

    def open_file(self, path, mode=None):
        if mode is None: mode = self.mode()
        self.file = open(path, mode=mode)

    def import_xml(self, xmlfile):
        if self.debug: print("Importing from", xmlfile)
        tree = None
        if self.rdonly:
            raise Exception("Can't import into read-only database")
        with open(xmlfile, mode='r') as f:
            tree = self.parser.parse(f)

        count = 0
        for xml in tree.getroot():
            if self.skippable_xml(xml): continue
            self.add_record(self.xml_to_record(xml))
            count += 1
        if self.debug:
            print("  Imported", count, "record(s); total",
                  len(self.db), "record(s)")
        return self

    def load(self):
        if self.debug: print("Loading from", self.path)
        db = yaml.loader.Loader(self.file).get_data()
        for key, rec in db.items():
            if "claim_number" in rec:
                if rec["claim_number"] != key:
                    raise Exception("database claim number mismatch! (%s != %s)" % (rec["claim_number"], key))
            else:
                rec["claim_number"] = key

        self.db = db
        if self.debug: print("  Loaded", len(self.db), "record(a)s")
        return self

    # Trying hard to do this safely
    def save(self):
        if self.rdonly:
            raise Exception("Can't save to read-only database")
        
        self.save_copy(self.tmpfile)
        try: os.unlink(self.backupfile)
        except FileNotFoundError: pass
        os.link(self.path, self.backupfile)
        os.rename(self.tmpfile, self.path)

    def save_copy(self, target_path):
        import sys
        with open(target_path, mode="w") as f:
            yaml.dump(self.db, f, default_flow_style=False)
        return self

    def skippable_xml(self, xml):
        # we expect there to be a row of TH cells
        # at the top of the input
        if xml.tag.lower() == 'tr':
            for child in xml:
                if child.tag.lower() != 'th':
                    return False
            return True
        else:
            return False
        
    # row is an Element object, should be
    # a TR element containing TD subelements
    def xml_to_record(self, row):
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

        return rec

    def add_record(self, rec):
        claim_number = rec["claim_number"]
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

    def alltext(self, elem):
        return "".join(elem.itertext())

if __name__ == '__main__':
    bdb = billdb("samples/arec.bdb", debug=True) \
        .import_xml("samples/a.xls").save()
#    from pprint import pprint as pp
#    pp(vars(bdb))
