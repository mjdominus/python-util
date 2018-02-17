#!/usr/bin/python3

class ResolutionException(Exception):
    def __init__(self, field, old, new):
        self.field = field
        self.old = old
        self.new = new

class resolver():
    # How to resolve merge conflicts in records
    # see resolve_conflict_for()
    #
    # elements here can be strings "update" or "ignore", or
    # a function that takes old and new values and
    # returns the merged result

    resolutions = { "status": "update" }

    def __init__(self):
        self.resolutions = self.__class__.resolutions

    def merge(self, old, new):
        merged = old.copy()

        # What can be merged?
        # Anything in the new record that is absent from the old is okay
        # Anything missing from the new record that is in the old is okay
        # Anything in the new record that exactly matches the old is okay
        # None values in the old record can be overwritten, None in the new record ignored

        # And there are a few special exceptions:
        #   Some status fields can be updated from new to old
        for key, val in new.items():
            if key not in merged or merged[key] is None:
                merged[key] = val
            elif val is None or val == merged[key]:
                pass
            else:
                merged[key] = self.resolve_conflict_for(key, merged, new)
        return merged
                
    def resolve_conflict_for(self, key, old, new):
        if key not in self.resolutions:
            raise ResolutionException(key, old[key], new[key])
        resolution = self.resolutions[key]
        if resolution == "update":
            return new[key]
        elif resolution == "ignore":
            return old[key]
        elif "__call__" in dir(resolution):
            return resolution.__call__(old, new)
        else:
            raise Exception("Unknown resolution '%s' for key '%s'" % (resolution, key))
        

