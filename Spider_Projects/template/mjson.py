import json
import collections


INDENT_SIZE = 4


class RWfile(object):

    def __init__(self, fname):
        self.fname = fname

    def write_in(self, raw_datas):
        clean_datas = json.dumps(
            raw_datas, ensure_ascii=False)
        with open(self.fname, 'w') as f:
            f.write(clean_datas)
        print("Write data to %s" % (self.fname))

    def read_out(self):
        with open(self.fname) as f:
            raw_datas = json.load(f, object_pairs_hook=collections.OrderedDict)
            clean_datas = json.dumps(
                raw_datas, indent=INDENT_SIZE, ensure_ascii=False)
        print("Read data from %s" % (self.fname))
        print(clean_datas)
