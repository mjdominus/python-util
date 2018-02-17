#!/usr/bin/python3

# import html.parser
from billdb.anthem_xml_importer import anthem_xml_importer
import yaml
import os

class billdb():

    # How to resolve merge conflicts in records
    # see resolve_conflict_for()
    #
    # elements here can be "update", "ignore", or
    # a function that takes old and new values and
    # returns the merged result
    resolutions = { }

    def __init__(self, path, rdonly=False, debug=False, tmpfile=None, backupfile=None,
                 xml_importer=None):
        if backupfile is None:
            self.backupfile = path + ".bkp"
        else:
            self.backupfile = backupfile
        self.db = {}
        self.debug = debug
        self.path = path
        self.rdonly = rdonly
        self.resolutions = self.__class__.resolutions
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
            self.merge_record(claim_number, rec)
            return 1
        else:
            self.db[claim_number] = rec
            return 0
    
    def get_claim(self, claim_number):
        self.db.get(claim_number)

    def has_claim(self, claim_number):
        return claim_number in self.db

    # Here we are presented with a new record
    # that has the same ID as an old record
    # Throws exception if it can't merge
    def merge_record(self, id, new):
        old = self.db[id]
        merged = old.copy()
        # What can be merged?
        # Anything in the new record that is absent from the old is okay
        # Anything in the new record that exactly matches the old is okay
        # Anything missing from the new record that is in the old is okay
        # None values in the new record can be ignored, None in the old record overwritten
        # And there are a few special exceptions:
        #   Some status fields can be updated from new to old
        #   Conceivably some information can be ignored in new when it mismatches
        #   The DB object can have a resolution policy
        for key, val in new.items():
            if key not in merged or merged[key] is None:
                merged[key] = val
            elif val is None or val == merged[key]:
                pass
            else:
                merged[key] = self.resolve_conflict_for(key, merged, new)
        return merged

    def resolve_conflict_for(self, key, old, new):
        try: resolution = self.resolutions[key]
        except KeyError:
            raise Exception("Conflict in '%s' field: old value <%s>, new value <%s>" % (key, old[key], new[key]))
        if resolution == "update":
            return new[key]
        elif resolution == "ignore":
            return old[key]
        elif "__call__" in dir(resolution):
            return resolution.__call__(old, new)
        else:
            raise Exception("Unknown resolution '%s' for key '%s'" % (resolution, key))
        
    def import_xml(self, xml_file):
        if self.rdonly:
            raise Exception("Can't import into read-only database")
        recs = self.xml_importer.import_xml(xml_file)
        merged = 0
        for rec in recs:
            merged += self.add_record(rec)
        if self.debug:
            print("  Added %d new record(s), merged %d" %
                  ( len(recs) - merged, merged ))
        return self

if __name__ == '__main__':
    bdb = billdb("samples/arec.bdb", debug=True,
                 xml_importer=anthem_xml_importer(debug=False)) \
        .import_xml("samples/a.xls").save()
#    from pprint import pprint as pp
#    pp(vars(bdb))
