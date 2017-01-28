
# coding: utf-8

# In[19]:

def conll_to_tokens(path_to_dataset, encoding='utf8'):
#     features = []
    labelled_tokens = []
    sent = []
    for line in open(path_to_dataset, 'r', encoding=encoding).readlines()[:20]:
#         if line == '':
#             features.append(sent)
#             sent = []
#         else:
#             chunks = line.split()
#             word_features = [chunks[0], chunks[2]]
# #             print(chunks[2:])
#             sent.append(([word_features], chunks[1]))
#     if len(sent) > 0:
#         features.append(sent)
        chunks = line.split()
        word_features = [chunks[0], chunks[2]]
        labelled_tokens.append(([word_features], chunks[1]))
    return labelled_tokens


# In[1]:

word2vec = {} # dictionary of word2vec representation of words


# In[2]:

symbols = {} # dictionary of one-hot encoded symbols


# In[11]:

pos_tags = {} # dictionary of word2vec representation of pos tags


# In[8]:

affix_ids = {} # dictionary of one-hot encoded suffixes and prefixes (word2vec???)


# In[10]:

def extract_features(labelled_tokens):  # @tokens - list of tokens, containing the tokens and its pos tag
    
    data = []
    for token, label in labelled_tokens:
        for symbol in token:
            features = []
            features.extend(word2vec[token])        # token word2vec
            features.extend(pos_tags[label])        # label word2vec
            features.extend(suffix_ids[token[-3:]]) # suffix code
            features.extend(suffix_ids[token[:3]])  # prefix code
            features.extend(symbols[symbol])        # symbol code
            features.append(symbol.isupper())       # upper/lower case
            features.append(symbol.isalpha())       # letter/symbol
            features.append(token[0].isupper())     # word's first letter's case
            features.append(token.isupper())        # word is all upper or not
            data.append((features, label))
    return data
            


# In[20]:

features = tokens_from_conll('ru1.conll.txt')


# In[23]:

features


# In[62]:

class Symbol:
    
    symbols = {'UNKN':[0.0, 0.0, 0.0]}   # dict of symbol one-hot codes
                    
    def __init__(self, symbol):
        self.value = symbol
        self.encoding = Symbol.symbols.get(symbol, Symbol.symbols['UNKN'])
        self.alphabetic = 1.0 if symbol.isalpha() else 0.0
    
    def get_features(self):
        x = self.encoding[:]
        x.append(self.alphabetic)
        return x


# In[104]:

class Token:
    
    tokens = {'UNKN':[0.0, 0.0, 0.0]}      # token word encodings
    tags = {'UNKN':[0.0, 0.0, 0.0]}        # tag encodings
    affixes = {'UNKN':[0.0, 0.0, 0.0]}     # affix encodings, (should we store code for prefixes and suffixes in the same dict?)
    
    def __init__(self, token, tag=None):
        
        self.value = token
        self.encoding = Token.tokens.get(token, Token.tokens['UNKN'])
        self.tag_value = tag
        self.tag_encoding = Token.tags.get(tag, Token.tags['UNKN'])
        self.suffix = Token.affixes.get(token[-3:], Token.affixes['UNKN'])
        self.prefix = Token.affixes.get(token[3:], Token.affixes['UNKN'])
        self.case = 1.0 if token[0].isupper() else 0.0
        self.upper = 1.0 if token.isupper() else 0.0
        self.symbols = list([Symbol(s) for s in token])
        
    def get_features(self):
        return self.encoding + self.tag_encoding + self.suffix + self.prefix + [self.case , self.upper]
    
    def get_symbol_features(self):
        return list([s.get_features() + self.get_features() for s in self.symbols])


# In[93]:

S = Symbol('a')


# In[94]:

print(S.get_features())


# In[105]:

t = Token('Привет')


# In[106]:

t.get_features()


# In[107]:

t.get_symbol_features()


# In[ ]:



