#!/usr/bin/python3

import xml.etree.ElementTree as ET

class xml_importer():
    
    def __init__(self, debug=False):
        self.parser = ET
        self.debug = debug
        self.conversions = {}

    def import_xml(self, xmlfile):
        if self.debug: print("Importing from", xmlfile)
        tree = None
        with open(xmlfile, mode='r') as f:
            tree = self.parser.parse(f)

        records = []
        for xml in tree.getroot():
            if self.skippable(xml): continue
            record = self.xml_to_record(xml)
            records.append(self.convert_record(record))
        if self.debug:
            print("  Imported", len(records), "record(s) from", xmlfile)
        return records

    def skippable(self, xml):
        return False
        
    # row is an Element object, should be
    # a TR element containing TD subelements
    def xml_to_record(self, xml):
        rec = {}
        rec["mystatus"]     = None
        rec["date_paid"]    = None
        rec["check_number"] = None
        rec["check_amount"] = None
        return rec

    def convert_record(self, rec):
        for key in rec:
            if key in self.conversions:
                old = rec[key]
                new = self.conversions[key](old)
                if (self.debug and old != new):
                    print("  Converted %s: <%s> to <%s>" % (key, old, new))
                rec[key] = new

        return rec

