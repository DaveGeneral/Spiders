import json
import collections


class RWfile(object):

    def __init__(self, fname):
        self.fname = fname

    def write_in(self, raw_datas):
        clean_datas = json.dumps(
            raw_datas, indent=4, ensure_ascii=False, sort_keys=False)
        with open(self.fname, 'w') as f:
            f.write(clean_datas)
        print("Data has been written to %s successfully!" % (self.fname))

    def read_out(self):
        with open(self.fname) as f:
            raw_datas = json.load(f, object_pairs_hook=collections.OrderedDict)
            clean_datas = json.dumps(raw_datas, indent=4, ensure_ascii=False)
        print(clean_datas)
