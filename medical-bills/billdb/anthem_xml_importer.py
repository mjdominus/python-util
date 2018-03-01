#!/usr/bin/python3

from billdb.xml_importer import xml_importer
from billdb.pii import pii
import re
import datetime

class anthem_xml_importer(xml_importer):

    sq = str.maketrans("", "", "'")
    sc = str.maketrans("", "", ",")
    money_pat = re.compile(r'\A \$ ( \d+\.\d\d ) \Z', flags=re.VERBOSE)

    def stripquotes(s):
        return s.translate(anthem_xml_importer.sq)

    def money(s):
        match = anthem_xml_importer.money_pat.match(s.translate(anthem_xml_importer.sc))
        if match is None:
            raise Exception("Dollar amount <%s> is malformed" % s)
        return match.group(1)
#       Or maybe:  return int(100 * float(match.group(1)))

    def date(s):
        return datetime.datetime.strptime(s, "%m/%d/%Y").date()

    def claim_type(s):
        if s.lower() in ["medical"]:
            return s
        else:
            raise Exception("Unexpected type <%s>" % s)

    def claimant(s):
        if s in pii.family:
            return pii.family[s]
        else:
            raise Exception("Unexpected claimant <%s>" % s)
        
    conversions = {
        "claim_id": stripquotes,
        "payable": money,
        "total": money,
        "date_service": date,
        "type": claim_type,
        "for": claimant,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversions = self.__class__.conversions
        
    def skippable(self, xml):
        # If the base method says to skip, we need do nothing further
        if super().skippable(xml):
            return True

        # we expect there to be a row of TH cells
        # at the top of the input
        if xml.tag.lower() == 'tr':
            for child in xml:
                if child.tag.lower() != 'th':
                    return False
            return True
        else:
            return False

    def xml_to_record(self, row):
        if row.tag.lower() != 'tr':
            raise Exception("Row had tag '" + row.tag +
                            "' instead of expected TR");

        rec = super().xml_to_record(row)
        
        rec["claim_id"] = self.unpack_td(row[0])
        rec["date_service"] = self.unpack_td(row[1])
        rec["for"]          = self.unpack_td(row[2])
        rec["type"]         = self.unpack_td(row[3])
        rec["doctor"]       = self.unpack_td(row[4])
        rec["total"]        = self.unpack_td(row[5])
        rec["payable"]      = self.unpack_td(row[6])
        rec["status"]       = self.unpack_td(row[7])

        return rec

    def unpack_td(self, elem):
        s = str(self.parser.tostring(elem))
        text = self.alltext(elem)
        if elem.tag != 'TD':
            raise Exception("element '" + s + "' has tag '" + elem.tag + "' instead of TD")
        elif text is None:
            raise Exception("element '" + s + "' has no text")
        return text
        
    def alltext(self, elem):
        return "".join(elem.itertext())

