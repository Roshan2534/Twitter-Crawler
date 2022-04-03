import pickle

filename = 'crowdsourced_keywords.pickle'

with open(filename, 'rb') as handle:
    data = pickle.load(handle)
    print(data)

