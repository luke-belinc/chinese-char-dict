import nltk
from nltk.corpus import treebank

sentence = "Hello, my name is Luke"

tokens = nltk.word_tokenize(sentence)

print("tokens: ", tokens)

tagged = nltk.pos_tag(tokens)

print("tags: ", tagged)

entities = nltk.chunk.ne_chunk(tagged)

print("entities: ", entities)

tree = treebank.parsed_sents('wsj_0001.mrg')[0]

tree.draw()
