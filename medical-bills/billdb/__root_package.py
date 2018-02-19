from billdb.anthem_xml_importer import anthem_xml_importer
from billdb.resolver import resolver, ResolutionException
import yaml
import os

class billdb():
    def __init__(self, path, rdonly=False, debug=False, tmpfile=None, backupfile=None,
                 xml_importer=anthem_xml_importer(),
                 conflict_resolver=resolver()):
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
            if "claim_id" in rec:
                if rec["claim_id"] != key:
                    raise Exception("database claim ID mismatch! (%s != %s)" % (rec["claim_id"], key))
            else:
                rec["claim_id"] = key

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
        claim_id = rec["claim_id"]
        if self.db.get(claim_id) is not None:
            if (self.merge_record(claim_id, rec)):
                return "merged"
            else:
                return "failed"
        else:
            self.db[claim_id] = rec
            return "added"
    
    def get_claim(self, claim_id):
        self.db.get(claim_id)

    def has_claim(self, claim_id):
        return claim_id in self.db

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


    def import_xml_from_file(self, path):
        recs = self.xml_importer.import_xml_from_file(path)
        self.import_recs(recs)

    def import_xml(self, xml_file):
        recs = self.xml_importer.import_xml(xml_file)
        self.import_recs(recs)

    def import_recs(self, recs):
        if self.rdonly:
            raise Exception("Can't import into read-only database")
        status = { "merged": 0, "added": 0, "failed": 0 }
        for rec in recs:
            result = self.add_record(rec)
            status[result] += 1
        if self.debug:
            for k in sorted(status.keys()):
                print("  %s: %d; " % (k, status[k]), end="")
            print()
        return self
