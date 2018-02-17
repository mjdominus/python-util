#!/usr/bin/python3

# import html.parser
from billdb.anthem_xml_importer import anthem_xml_importer
from billdb.resolver import resolver, ResolutionException
import yaml
import os

class billdb():

    def __init__(self, path, rdonly=False, debug=False, tmpfile=None, backupfile=None,
                 xml_importer=None,
                 conflict_resolver=None):
        if backupfile is None:
            self.backupfile = path + ".bkp"
        else:
            self.backupfile = backupfile
        self.conflict_resolver = conflict_resolver
        self.db = {}
        self.debug = debug
        self.path = path
        self.rdonly = rdonly
        if tmpfile is None:
            self.tmpfile = path + ".tmp"
        else:
            self.tmpfile = tmpfile
        self.xml_importer = xml_importer

        self.open_file(self.path)
        self.load()

    def mode(self):
        if self.rdonly: return "r"
        else: return "r+"

    def open_file(self, path, mode=None):
        if mode is None: mode = self.mode()
        self.file = open(path, mode=mode)

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
        if self.debug: print("  Loaded", len(self.db), "record(s)")
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
        
        with open(target_path, mode="w") as f:
            yaml.dump(self.db, f, default_flow_style=False)
        return self

    def add_record(self, rec):
        claim_number = rec["claim_number"]
        if self.db.get(claim_number) is not None:
            if (self.merge_record(claim_number, rec)):
                return "merged"
            else:
                return "failed"
        else:
            self.db[claim_number] = rec
            return "added"
    
    def get_claim(self, claim_number):
        self.db.get(claim_number)

    def has_claim(self, claim_number):
        return claim_number in self.db

    # Here we are presented with a new record
    # that has the same ID as an old record
    # Throws exception if it can't merge
    def merge_record(self, id, new):
        try:
            self.db[id] = self.conflict_resolver.merge(self.db[id], new)
            return True
        except ResolutionException as exc:
            print("Record <%s> has a conflicting '%s' value <%s>; was <%s>; ignoring!" %
                  (id, exc.field, exc.old, exc.new))
            return False


    def import_xml(self, xml_file):
        if self.rdonly:
            raise Exception("Can't import into read-only database")
        recs = self.xml_importer.import_xml(xml_file)
        status = { "merged": 0, "added": 0, "failed": 0 }
        for rec in recs:
            result = self.add_record(rec)
            status[result] += 1
        if self.debug:
            for k in sorted(status.keys()):
                print("  %s: %d; " % (k, status[k]), end="")
            print()
        return self

if __name__ == '__main__':
    bdb = billdb("samples/arec.bdb", debug=True,
                 xml_importer=anthem_xml_importer(debug=False),
                 conflict_resolver=resolver()) \
        .import_xml("samples/a.xls").save()
#    from pprint import pprint as pp
#    pp(vars(bdb))
