import os
import json

def getEntries():
    # annoying workaround for 'file not found' error
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(THIS_FOLDER, 'dictionary.txt')

    # open file
    f = open(file, "r")

    # parse lines from file into json objects
    entries = []
    for line in f:
        e = json.loads(line)
        entries.append(e)

    #return json object array 
    return entries