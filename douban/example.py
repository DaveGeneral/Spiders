import json
from collections import OrderedDict
with open('output.json') as data_file:
    data = json.load(data_file)
    mydata = json.dumps(data, indent=4, ensure_ascii=False,
                        object_pairs_hook=OrderedDict)
print(len(data))
print(data['5']['Comment'])
print(mydata)
