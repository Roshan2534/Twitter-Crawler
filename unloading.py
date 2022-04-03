import pickle
import json

filename = 'crowdsourced_keywords.pickle'

f = open(filename, 'rb')
newdict = json.dumps(pickle.load(f))
print(newdict)
f.close()


