import json
import collections


INDENT_SIZE = 2


class RWfile(object):

    def __init__(self, fname):
        self.fname = fname

    def write_in(self, raw):
        clean = json.dumps(raw, indent=INDENT_SIZE, ensure_ascii=False)
        with open(self.fname, 'w') as f:
            f.write(clean)
        print("Write data to %s" % (self.fname))

    def read_out(self):
        with open(self.fname) as f:
            raw = json.load(f, object_pairs_hook=collections.OrderedDict)
            clean = json.dumps(
                raw, indent=INDENT_SIZE, ensure_ascii=False)
        print("Read data from %s" % (self.fname))
        print(clean)
