import json
with open('xe.json') as data_file:
    data = json.load(data_file)
    mydata = json.dumps(data, indent=2)
print(data)
print(len(data))
print(data['rank1']['name'])
print(mydata)
